"""Onglet Tâches & Notes."""
from __future__ import annotations

import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from database import Database
from models import Task


class TasksTab:
    def __init__(self, parent: tk.Widget, app: object) -> None:
        self.app = app
        self.db: Database = app.db
        self.frame = ttk.Frame(parent)
        self._build()

    def _build(self) -> None:
        top = ttk.Frame(self.frame)
        top.pack(fill=tk.X, padx=8, pady=6)

        ttk.Button(top, text="Nouvelle tâche", command=self.create_task).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="Nouvelle note", command=self.create_note).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="Actualiser", command=self.refresh).pack(side=tk.LEFT, padx=4)

        middle = ttk.PanedWindow(self.frame, orient=tk.HORIZONTAL)
        middle.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)

        # Tasks
        task_frame = ttk.Frame(middle)
        middle.add(task_frame, weight=1)
        ttk.Label(task_frame, text="Tâches").pack()
        self.tasks_tree = ttk.Treeview(
            task_frame, columns=("estimate", "done", "start", "end", "status"), show="headings"
        )
        for col in ("estimate", "done", "start", "end", "status"):
            self.tasks_tree.heading(col, text=col)
        self.tasks_tree.pack(fill=tk.BOTH, expand=True)
        self.tasks_tree.bind("<Double-1>", self._on_task_double)

        # Notes
        note_frame = ttk.Frame(middle)
        middle.add(note_frame, weight=1)
        ttk.Label(note_frame, text="Notes").pack()
        self.notes_listbox = tk.Listbox(note_frame)
        self.notes_listbox.pack(fill=tk.BOTH, expand=True)

    def _current_project_id(self) -> int | None:
        return self.app.selected_project_id

    def create_task(self) -> None:
        project_id = self._current_project_id()
        if project_id is None:
            messagebox.showinfo("Info", "Sélectionner un projet d'abord")
            return
        title = simpledialog.askstring("Nouvelle tâche", "Titre:")
        if not title:
            return
        est = simpledialog.askfloat("Estimation (h)", "Heures estimées:", minvalue=0.0, initialvalue=1.0)
        start = simpledialog.askstring("Date début", "Date début (YYYY-MM-DD) - optionnelle:")
        end = simpledialog.askstring("Date fin", "Date fin (YYYY-MM-DD) - optionnelle:")
        self.db.add_task(
            project_id=project_id,
            title=title,
            estimate_hours=float(est) if est else 0.0,
            start=start or None,
            end=end or None,
        )
        self.refresh()

    def create_note(self) -> None:
        project_id = self._current_project_id()
        if project_id is None:
            messagebox.showinfo("Info", "Sélectionner un projet d'abord")
            return
        content = simpledialog.askstring("Nouvelle note", "Contenu:")
        if not content:
            return
        self.db.add_note(project_id=project_id, content=content)
        self.refresh()

    def refresh(self) -> None:
        project_id = self._current_project_id()
        # tasks
        for i in self.tasks_tree.get_children():
            self.tasks_tree.delete(i)
        if project_id is None:
            return
        tasks = self.db.list_tasks(project_id=project_id)
        for t in tasks:
            status = "Terminé" if t.completed else "En cours"
            self.tasks_tree.insert(
                "",
                "end",
                iid=str(t.id),
                values=(t.estimate_hours, t.done_hours, t.start or "", t.end or "", status),
            )
        # notes
        self.notes_listbox.delete(0, tk.END)
        notes = self.db.list_notes(project_id=project_id)
        for n in notes:
            self.notes_listbox.insert(tk.END, f"{n.created_at[:19]} - {n.content[:80]}")

    def _on_task_double(self, event: object) -> None:
        iid = self.tasks_tree.focus()
        if not iid:
            return
        task_id = int(iid)
        task = self.db.get_task(task_id)
        if not task:
            return
        done = simpledialog.askfloat(
            "Heures réalisées",
            "Heures réalisées jusqu'à présent:",
            initialvalue=getattr(task, "done_hours", 0.0),
            minvalue=0.0,
        )
        completed = messagebox.askyesno("Terminé?", "Marquer la tâche comme terminée ?")
        upd = {"done_hours": float(done) if done is not None else getattr(task, "done_hours", 0.0), "completed": completed}
        if completed and not getattr(task, "end", None):
            upd["end"] = datetime.date.today().isoformat()
        self.db.update_task(task_id, **upd)

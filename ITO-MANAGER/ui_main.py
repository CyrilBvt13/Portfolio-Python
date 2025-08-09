"""Fenêtre principale et navigation entre onglets.

Déléguons le contenu des onglets à des modules séparés `ui_tasks` et `ui_graphs`.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox

from database import Database
from ui_tasks import TasksTab
from ui_graphs import GraphsTab


class InteropManagerApp(tk.Tk):
    def __init__(self, db: Database) -> None:
        super().__init__()
        self.title("Interop Project Manager")
        self.geometry("1100x700")
        self.db = db

        self.projects = []
        self.selected_project_id: int | None = None

        self._create_widgets()
        self._refresh_projects()

    def _create_widgets(self) -> None:
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(paned, width=280)
        right_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        paned.add(right_frame, weight=4)

        ttk.Label(left_frame, text="Projets", font=(None, 12, "bold")).pack(padx=8, pady=6)

        self.proj_listbox = tk.Listbox(left_frame)
        self.proj_listbox.pack(fill=tk.BOTH, expand=True, padx=8)
        self.proj_listbox.bind("<<ListboxSelect>>", self._on_project_select)

        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, pady=6, padx=8)

        ttk.Button(btn_frame, text="Nouveau projet", command=self._create_project).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Supprimer", command=self._delete_project).pack(side=tk.LEFT, padx=4)

        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tabs
        self.tasks_tab = TasksTab(self.notebook, self)
        self.notebook.add(self.tasks_tab.frame, text="Tâches & Notes")

        self.graphs_tab = GraphsTab(self.notebook, self)
        self.notebook.add(self.graphs_tab.frame, text="Suivi graphique")

    # Project actions
    def _create_project(self) -> None:
        from tkinter import simpledialog

        name = simpledialog.askstring("Nouveau projet", "Nom du projet:")
        if not name:
            return
        desc = simpledialog.askstring("Description", "Description (optionnelle):") or ""
        proj = self.db.add_project(name=name, description=desc)
        self._refresh_projects()
        self._select_project_in_list(proj.id)

    def _refresh_projects(self) -> None:
        self.proj_listbox.delete(0, tk.END)
        self.projects = self.db.list_projects()
        for p in self.projects:
            self.proj_listbox.insert(tk.END, f"{p.id} - {p.name}")

    def _select_project_in_list(self, project_id: int) -> None:
        for idx, p in enumerate(self.projects):
            if p.id == project_id:
                self.proj_listbox.selection_clear(0, tk.END)
                self.proj_listbox.selection_set(idx)
                self.proj_listbox.see(idx)
                self._on_project_select()
                return

    def _delete_project(self) -> None:
        sel = self.proj_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        proj = self.projects[idx]
        if not messagebox.askyesno("Supprimer", f"Supprimer le projet {proj.name} ?"):
            return
        self.db.remove_project(proj.id)
        self.selected_project_id = None
        self._refresh_projects()
        self.tasks_tab.refresh()
        self.graphs_tab.draw()

    def _on_project_select(self, event: object | None = None) -> None:
        sel = self.proj_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        proj = self.projects[idx]
        self.selected_project_id = proj.id
        # notify tabs
        self.tasks_tab.refresh()
        self.graphs_tab.draw()

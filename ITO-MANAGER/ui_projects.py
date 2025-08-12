"""Onglet de gestion des projets (liste, ajout, modification, suppression)."""
from __future__ import annotations

import tkinter as tk
from tkinter import simpledialog, messagebox
from typing import Callable

from database import Database
from models import Project


class ProjectsFrame(tk.Frame):
    """Liste des projets avec actions CRUD."""

    def __init__(self, master, db: Database, on_project_selected: Callable[[Project], None]) -> None:
        super().__init__(master, width=300)
        self.db = db
        self.on_project_selected = on_project_selected

        tk.Label(self, text="Projets", font=("Arial", 14, "bold")).pack(pady=6)

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=4)
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=6, padx=4)

        tk.Button(btn_frame, text="Ajouter", command=self.add_project).pack(side=tk.LEFT, expand=True, padx=2)
        tk.Button(btn_frame, text="Modifier", command=self.edit_project).pack(side=tk.LEFT, expand=True, padx=2)
        tk.Button(btn_frame, text="Supprimer", command=self.delete_project).pack(side=tk.LEFT, expand=True, padx=2)

        self.refresh()

    def refresh(self) -> None:
        """Recharge la liste des projets depuis la base (affiche uniquement le nom)."""
        self.listbox.delete(0, tk.END)
        self.projects = self.db.list_projects()
        for p in self.projects:
            # affiche seulement le nom (sans pourcentage)
            self.listbox.insert(tk.END, f"{p.name}")

    def _on_select(self, event) -> None:
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        project = self.projects[idx]
        # callback vers l'application
        self.on_project_selected(project)

    def add_project(self) -> None:
        name = simpledialog.askstring("Nouveau projet", "Nom du projet :")
        if not name:
            return
        self.db.add_project(name)
        self.refresh()

    def edit_project(self) -> None:
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Info", "Sélectionner un projet à modifier.")
            return
        idx = sel[0]
        project = self.projects[idx]
        new_name = simpledialog.askstring("Modifier projet", "Nouveau nom :", initialvalue=project.name)
        if not new_name:
            return
        project.name = new_name
        self.db.update_project(project)
        self.refresh()

    def delete_project(self) -> None:
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Info", "Sélectionner un projet à supprimer.")
            return
        idx = sel[0]
        project = self.projects[idx]
        if messagebox.askyesno("Confirmation", f"Supprimer le projet '{project.name}' ?"):
            self.db.delete_project(project.id)
            self.refresh()

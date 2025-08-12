"""Interface principale — fenêtre et onglets.

La fenêtre principale utilise TkinterDnD.Tk pour activer le drag & drop
depuis l'OS vers les formulaires de note.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

# TkinterDnD provides native-like drag & drop support for Tkinter.
from tkinterdnd2 import TkinterDnD

from ui_projects import ProjectsFrame
from ui_notes import NotesFrame
from database import Database


class MainApp(TkinterDnD.Tk):
    """Fenêtre principale de l'application."""

    def __init__(self, db: Database) -> None:
        super().__init__()
        self.db = db
        self.title("Interop Manager")
        self.geometry("1000x650")

        # Frame gauche: projets
        self.projects_frame = ProjectsFrame(self, db, self.on_project_selected)
        self.projects_frame.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)

        # Zone de droite: onglets (pour extension future)
        right = ttk.Frame(self)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=8, pady=8)

        # For now we keep a single Notes tab; future tabs can be added easily.
        self.notes_frame = NotesFrame(right, db)
        self.notes_frame.pack(fill=tk.BOTH, expand=True)

    def on_project_selected(self, project) -> None:
        """Callback quand un projet est sélectionné dans la colonne de gauche."""
        self.notes_frame.set_project(project)

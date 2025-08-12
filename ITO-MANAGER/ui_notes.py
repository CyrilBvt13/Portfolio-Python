"""Onglet Notes avec support multiple attachments (.msg) et DnD dans le formulaire.

Le drag & drop est lié au formulaire d'ajout/modification (Toplevel) pour faciliter
l'attachement multiple lors de la création/modif.
"""
from __future__ import annotations

import os
import platform
import subprocess
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

from tkinterdnd2 import DND_FILES

from database import Database
from models import Note


def _open_file(path: str) -> None:
    """Ouvre un fichier avec l'application système par défaut."""
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.run(["open", path], check=False)
        else:
            subprocess.run(["xdg-open", path], check=False)
    except Exception as exc:
        messagebox.showerror("Erreur", f"Impossible d'ouvrir le fichier : {exc}")


class NoteForm(tk.Toplevel):
    """Formulaire pour ajouter / modifier une note.

    Supporte drop de plusieurs fichiers .msg. Chaque drop ajoute au lot d'attachements.
    """

    def __init__(self, master, db: Database, project_id: int, on_saved, note: Note | None = None) -> None:
        super().__init__(master)
        self.db = db
        self.project_id = project_id
        self.on_saved = on_saved
        self.note = note

        self.title("Modifier la note" if note else "Nouvelle note")
        self.geometry("600x480")

        self.attachments: list[str] = list(note.attachments) if note else []

        tk.Label(self, text="Contenu :", font=("Arial", 11)).pack(anchor="w", padx=8, pady=(8, 0))
        self.text = tk.Text(self, height=12, wrap="word")
        self.text.pack(fill=tk.BOTH, expand=False, padx=8, pady=(0, 6))

        if note:
            self.text.insert("1.0", note.content)

        # Drop area
        drop_frame = tk.Frame(self, relief="ridge", bd=1)
        drop_frame.pack(fill=tk.X, padx=8, pady=6)
        drop_label = tk.Label(drop_frame, text="Déposer un ou plusieurs .msg ici pour les ajouter", pady=8)
        drop_label.pack(fill=tk.X)
        # register drop target on label
        drop_label.drop_target_register(DND_FILES)
        drop_label.dnd_bind("<<Drop>>", self._on_drop)

        # Attachments list with remove buttons
        self.attach_container = tk.Frame(self)
        self.attach_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)
        self._render_attachments()

        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=8, pady=8)
        ttk.Button(btn_frame, text="Enregistrer", command=self._save).pack(side=tk.RIGHT, padx=4)
        ttk.Button(btn_frame, text="Annuler", command=self.destroy).pack(side=tk.RIGHT, padx=4)

    def _render_attachments(self) -> None:
        """Affiche la liste des attachments avec boutons pour ouvrir/supprimer."""
        for w in self.attach_container.winfo_children():
            w.destroy()

        if not self.attachments:
            tk.Label(self.attach_container, text="Aucun fichier attaché.").pack(anchor="w")
            return

        for path in self.attachments:
            row = tk.Frame(self.attach_container)
            row.pack(fill=tk.X, pady=2)
            lbl = tk.Label(row, text=os.path.basename(path), anchor="w")
            lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)
            tk.Button(row, text="Ouvrir", command=lambda p=path: _open_file(p)).pack(side=tk.RIGHT, padx=2)
            tk.Button(row, text="Supprimer", command=lambda p=path: self._remove_attachment(p)).pack(side=tk.RIGHT, padx=2)

    def _remove_attachment(self, path: str) -> None:
        """Retire un chemin de la liste d'attachments et rafraîchit l'affichage."""
        if path in self.attachments:
            self.attachments.remove(path)
            self._render_attachments()

    def _on_drop(self, event) -> None:
        """Handler du DnD: accepte plusieurs fichiers, prend uniquement les .msg existants."""
        raw = event.data
        # parse possible patterns like '{C:\a.msg} {C:\b.msg}'
        paths = []
        cur = ""
        in_brace = False
        for ch in raw:
            if ch == "{":
                in_brace = True
                cur = ""
            elif ch == "}":
                in_brace = False
                paths.append(cur)
            elif in_brace:
                cur += ch
        if not paths:
            # fallback: single path without braces
            paths = [raw.strip()]

        for p in paths:
            p = p.strip().strip("{}").strip()
            p = os.path.expanduser(p)
            if os.path.isfile(p) and p.lower().endswith(".msg"):
                ap = os.path.abspath(p)
                if ap not in self.attachments:
                    self.attachments.append(ap)
            else:
                messagebox.showwarning("Fichier ignoré", f"Le fichier {p} est ignoré (pas un .msg ou introuvable)")
        self._render_attachments()

    def _save(self) -> None:
        """Enregistre la note (création ou modification)."""
        content = self.text.get("1.0", "end").strip()
        if not content:
            messagebox.showinfo("Info", "Le contenu de la note est vide.")
            return
        if self.note:
            # update existing
            self.note.content = content
            self.note.attachments = list(self.attachments)
            self.db.update_note(self.note)
        else:
            self.db.add_note(self.project_id, content, list(self.attachments))
        self.on_saved()
        self.destroy()


class NotesFrame(tk.Frame):
    """Affiche et gère les notes d'un projet."""

    def __init__(self, master, db: Database) -> None:
        super().__init__(master)
        self.db = db
        self.project_id: int | None = None

        tk.Label(self, text="Notes du projet", font=("Arial", 14, "bold")).pack(pady=6)

        # Container des notes (lignes dynamiques)
        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True, padx=6)

        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=6)
        tk.Button(btn_frame, text="Nouvelle note", command=self._open_new_note).pack(side=tk.LEFT, padx=4)

        self.refresh_notes()

    def set_project(self, project) -> None:
        """Associe la frame à un projet et recharge les notes."""
        self.project_id = project.id
        self.refresh_notes()

    def refresh_notes(self) -> None:
        """Recharge l'affichage des notes pour le projet courant."""
        for w in self.container.winfo_children():
            w.destroy()

        if self.project_id is None:
            return

        notes = self.db.list_notes(project_id=self.project_id)
        for note in notes:
            row = tk.Frame(self.container, relief="groove", bg="white", bd=1)
            row.pack(fill=tk.X, pady=4, padx=2)

            txt = note.content if len(note.content) < 160 else note.content[:160] + "…"
            lbl = tk.Label(row, text=txt, anchor="w", justify="left", bg="white", wraplength=700)
            lbl.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6, pady=6)

            # attachments summary
            if note.attachments:
                att_btn = tk.Button(row, text=f"📎 {len(note.attachments)} pièce(s)", command=lambda n=note: self._show_attachments(n))
                att_btn.pack(side=tk.RIGHT, padx=4)

            tk.Button(row, text="🗑 Supprimer", command=lambda n=note: self._delete_note(n)).pack(side=tk.RIGHT, padx=4)
            tk.Button(row, text="✏ Modifier", command=lambda n=note: self._open_edit_note(n)).pack(side=tk.RIGHT, padx=4)

    def _show_attachments(self, note: Note) -> None:
        """Affiche une petite fenêtre listant les attachments et permettant d'ouvrir chacun."""
        top = tk.Toplevel(self)
        top.title("Attachments")
        top.geometry("400x200")
        for p in note.attachments:
            frame = tk.Frame(top)
            frame.pack(fill=tk.X, pady=2, padx=4)
            lbl = tk.Label(frame, text=os.path.basename(p), anchor="w")
            lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)
            tk.Button(frame, text="Ouvrir", command=lambda pp=p: _open_file(pp)).pack(side=tk.RIGHT, padx=4)

    def _open_new_note(self) -> None:
        if self.project_id is None:
            messagebox.showinfo("Info", "Sélectionner un projet d'abord.")
            return
        NoteForm(self.master, self.db, self.project_id, on_saved=self.refresh_notes)

    def _open_edit_note(self, note: Note) -> None:
        NoteForm(self.master, self.db, self.project_id, on_saved=self.refresh_notes, note=note)

    def _delete_note(self, note: Note) -> None:
        if messagebox.askyesno("Confirmation", "Supprimer cette note ?"):
            self.db.delete_note(note.id)
            self.refresh_notes()

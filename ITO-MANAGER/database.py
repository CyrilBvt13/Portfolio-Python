"""Gestion TinyDB: CRUD pour projets et notes (attachments list)."""
from __future__ import annotations

from typing import Optional, List
from dataclasses import asdict

from tinydb import TinyDB, Query

from models import Project, Note


class Database:
    """Wrapper simple autour de TinyDB pour gérer projets et notes.

    Stores attachments as lists of absolute paths in the Note dataclass.
    """

    def __init__(self, path: str = "interop_db.json") -> None:
        self._db = TinyDB(path)
        self.projects = self._db.table("projects")
        self.notes = self._db.table("notes")
        self._meta = self._db.table("meta")

        meta_q = Query()
        if not self._meta.get(meta_q.id == 1):
            # stocke un document meta unique avec id==1
            self._meta.insert({"id": 1, "next_id": 1})

    def _get_next_id(self) -> int:
        """Renvoie et incrémente l'ID suivant."""
        meta_q = Query()
        meta = self._meta.get(meta_q.id == 1)
        next_id = meta.get("next_id", 1)
        self._meta.update({"next_id": next_id + 1}, meta_q.id == 1)
        return next_id

    # Projects
    def add_project(self, name: str) -> Project:
        """Ajoute un projet et le retourne."""
        pid = self._get_next_id()
        proj = Project(id=pid, name=name)
        self.projects.insert(asdict(proj))
        return proj

    def list_projects(self) -> List[Project]:
        """Retourne la liste des projets."""
        return [Project(**p) for p in self.projects.all()]

    def get_project(self, project_id: int) -> Optional[Project]:
        row = self.projects.get(Query().id == project_id)
        return Project(**row) if row else None

    def update_project(self, project: Project) -> None:
        q = Query()
        self.projects.update(asdict(project), q.id == project.id)

    def delete_project(self, project_id: int) -> None:
        q = Query()
        self.projects.remove(q.id == project_id)
        # supprime aussi les notes liées
        self.notes.remove(q.project_id == project_id)

    # Notes
    def add_note(self, project_id: int, content: str, attachments: Optional[List[str]] = None) -> Note:
        """Ajoute une note. attachments peut être une liste de chemins."""
        nid = self._get_next_id()
        attachments = attachments or []
        note = Note(id=nid, project_id=project_id, content=content, attachments=attachments)
        self.notes.insert(asdict(note))
        return note

    def list_notes(self, project_id: int | None = None) -> List[Note]:
        """Liste les notes, filtrées par projet si demandé."""
        if project_id is None:
            rows = self.notes.all()
        else:
            rows = self.notes.search(Query().project_id == project_id)
        return [Note(**r) for r in rows]

    def get_note(self, note_id: int) -> Optional[Note]:
        row = self.notes.get(Query().id == note_id)
        return Note(**row) if row else None

    def update_note(self, note: Note) -> None:
        q = Query()
        self.notes.update(asdict(note), q.id == note.id)

    def delete_note(self, note_id: int) -> None:
        q = Query()
        self.notes.remove(q.id == note_id)

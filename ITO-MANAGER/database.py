"""Wrapper simple autour de TinyDB pour CRUD minimal.

Les fonctions renvoient/consomment des dictionnaires compatibles avec
les dataclasses définies dans `models.py`.
"""
from __future__ import annotations

from typing import Optional

from tinydb import TinyDB, Query

from models import Project, Task, Note


class Database:
    def __init__(self, path: str = "interop_db.json") -> None:
        self._db = TinyDB(path)
        self._projects = self._db.table("projects")
        self._tasks = self._db.table("tasks")
        self._notes = self._db.table("notes")
        self._meta = self._db.table("meta")
        MetaQuery = Query()
        if not self._meta.get(MetaQuery.id == 1):
            self._meta.upsert({"id": 1, "next_id": 1}, MetaQuery.id == 1)


    def _next_id(self) -> int:
        row = self._meta.get(doc_id=1)
        nid = row.get("next_id", 1)
        self._meta.update({"next_id": nid + 1}, doc_ids=[1])
        return nid

    # Projects
    def add_project(self, name: str, description: str = "") -> Project:
        pid = self._next_id()
        proj = Project(id=pid, name=name, description=description)
        self._projects.insert(proj.__dict__)
        return proj

    def list_projects(self) -> list[Project]:
        return [Project(**p) for p in self._projects.all()]

    def get_project(self, project_id: int) -> Optional[Project]:
        row = self._projects.get(Query().id == project_id)
        return Project(**row) if row else None

    def remove_project(self, project_id: int) -> None:
        self._projects.remove(Query().id == project_id)
        self._tasks.remove(Query().project_id == project_id)
        self._notes.remove(Query().project_id == project_id)

    # Tasks
    def add_task(
        self,
        project_id: int,
        title: str,
        estimate_hours: float = 0.0,
        start: str | None = None,
        end: str | None = None,
    ) -> Task:
        tid = self._next_id()
        task = Task(
            id=tid,
            project_id=project_id,
            title=title,
            estimate_hours=estimate_hours,
            start=start,
            end=end,
        )
        self._tasks.insert(task.__dict__)
        return task

    def update_task(self, task_id: int, **fields) -> None:
        self._tasks.update(fields, Query().id == task_id)

    def list_tasks(self, project_id: int | None = None) -> list[Task]:
        if project_id is None:
            rows = self._tasks.all()
        else:
            rows = self._tasks.search(Query().project_id == project_id)
        return [Task(**r) for r in rows]

    def get_task(self, task_id: int) -> Optional[Task]:
        row = self._tasks.get(Query().id == task_id)
        return Task(**row) if row else None

    # Notes
    def add_note(self, project_id: int, content: str) -> Note:
        nid = self._next_id()
        note = Note(id=nid, project_id=project_id, content=content)
        self._notes.insert(note.__dict__)
        return note

    def list_notes(self, project_id: int | None = None) -> list[Note]:
        if project_id is None:
            rows = self._notes.all()
        else:
            rows = self._notes.search(Query().project_id == project_id)
        return [Note(**r) for r in rows]

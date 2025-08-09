import os
import json
from pathlib import Path

import pytest

from database import Database

def test_add_project_task_note(tmp_path):
    db_path = tmp_path / "test_db.json"
    db = Database(path=str(db_path))

    # add project
    proj = db.add_project("Test Project", "desc")
    assert proj.id is not None
    projects = db.list_projects()
    assert any(p.id == proj.id for p in projects)

    # add task
    task = db.add_task(proj.id, "Tâche 1", estimate_hours=5.0)
    assert task.project_id == proj.id
    tasks = db.list_tasks(project_id=proj.id)
    assert any(t.id == task.id for t in tasks)

    # add note
    note = db.add_note(proj.id, "Note 1")
    notes = db.list_notes(project_id=proj.id)
    assert any(n.id == note.id for n in notes)

def test_update_and_remove(tmp_path):
    db_path = tmp_path / "test_db2.json"
    db = Database(path=str(db_path))

    proj = db.add_project("P2")
    t = db.add_task(proj.id, "T2", estimate_hours=3.0)
    db.update_task(t.id, done_hours=1.5, completed=True)
    updated = db.get_task(t.id)
    assert updated.done_hours == 1.5
    assert updated.completed is True

    db.remove_project(proj.id)
    assert db.list_tasks(project_id=proj.id) == []
    assert db.list_notes(project_id=proj.id) == []

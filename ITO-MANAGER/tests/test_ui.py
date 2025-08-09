import pytest
pytest.importorskip("tkinter")
import tkinter as tk
from pathlib import Path

from database import Database
from ui_tasks import TasksTab

def test_tasks_tab_smoke(tmp_path):
    db_path = tmp_path / "ui_db.json"
    db = Database(path=str(db_path))
    proj = db.add_project("UIProj")
    # create root
    root = tk.Tk()
    # dummy app with required attributes
    class DummyApp:
        def __init__(self, db, project_id):
            self.db = db
            self.selected_project_id = project_id

    app = DummyApp(db, proj.id)
    tab = TasksTab(root, app)
    # should be able to refresh without raising
    tab.refresh()
    root.destroy()

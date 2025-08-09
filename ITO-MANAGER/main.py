"""Point d'entrée de l'application."""
from __future__ import annotations

from tinydb import TinyDB

from database import Database
from ui_main import InteropManagerApp
from utils import ensure_requirements_installed


def main() -> None:
    """Lancer l'application."""
    ensure_requirements_installed()
    db = Database(path="interop_db.json")
    app = InteropManagerApp(db)
    app.mainloop()


if __name__ == "__main__":
    main()

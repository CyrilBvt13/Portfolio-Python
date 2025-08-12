"""Point d'entrée de l'application."""
from __future__ import annotations

from database import Database
from ui_main import MainApp


def main() -> None:
    """Lance l'application."""
    db = Database(path="interop_db.json")
    app = MainApp(db)
    app.mainloop()


if __name__ == "__main__":
    main()

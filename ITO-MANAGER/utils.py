"""Fonctions utilitaires.

Ne fait pas d'installation automatique — affiche un message si dépendances manquantes.
"""
from __future__ import annotations


def ensure_requirements_installed() -> None:
    try:
        import tinydb  # noqa: F401
        import matplotlib  # noqa: F401
    except Exception:  # pragma: no cover - helper
        msg = (
            "Modules manquants: installez les dépendances avec:\n"
            "pip install tinydb matplotlib"
        )
        print(msg)

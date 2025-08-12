"""Fonctions utilitaires (petites helpers)."""
from __future__ import annotations

import os
import sys


def resource_path(relative: str) -> str:
    """Return absolute path for bundled resources (helper for packaging)."""
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, relative)

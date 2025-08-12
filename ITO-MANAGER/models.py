"""Modèles de données (dataclasses)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional
import datetime


def _now_iso() -> str:
    return datetime.datetime.utcnow().isoformat()


@dataclass
class Project:
    """Représente un projet minimal."""
    id: int
    name: str
    progress: int = 0  # valeur interne, non affichée dans la liste


@dataclass
class Note:
    """Représente une note liée à un projet.

    attachments: liste de chemins absolus vers des fichiers (.msg).
    """
    id: int
    project_id: int
    content: str
    created_at: str = field(default_factory=_now_iso)
    attachments: List[str] = field(default_factory=list)

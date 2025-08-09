"""Définitions des modèles utilisés par l'application.

Utilisation de dataclasses pour clarté et sérialisation simple.
"""
from __future__ import annotations

import datetime
from dataclasses import dataclass, field


def _now_iso() -> str:
    return datetime.datetime.utcnow().isoformat()


@dataclass
class Project:
    id: int
    name: str
    description: str = ""
    created_at: str = field(default_factory=_now_iso)


@dataclass
class Task:
    id: int
    project_id: int
    title: str
    estimate_hours: float = 0.0
    done_hours: float = 0.0
    start: str | None = None
    end: str | None = None
    completed: bool = False


@dataclass
class Note:
    id: int
    project_id: int
    content: str
    created_at: str = field(default_factory=_now_iso)

"""Onglet graphique: Gantt + reste à faire.

La génération des graphiques utilise matplotlib intégré dans Tkinter.
"""
from __future__ import annotations

import datetime
import threading
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import date2num
from matplotlib.figure import Figure
from tkinter import ttk

from database import Database


class GraphsTab:
    def __init__(self, parent: tk.Widget, app: object) -> None:
        self.app = app
        self.db: Database = app.db
        self.frame = ttk.Frame(parent)
        self._build()

    def _build(self) -> None:
        top = ttk.Frame(self.frame)
        top.pack(fill=tk.X, padx=8, pady=6)
        ttk.Button(top, text="Rafraîchir graphiques", command=self.draw).pack(side=tk.LEFT, padx=4)

        self.fig = Figure(figsize=(8, 6), tight_layout=True)
        self.ax_gantt = self.fig.add_subplot(211)
        self.ax_bar = self.fig.add_subplot(212)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _current_project_id(self) -> int | None:
        return self.app.selected_project_id

    def draw(self) -> None:
        threading.Thread(target=self._draw_worker, daemon=True).start()

    def _draw_worker(self) -> None:
        project_id = self._current_project_id()
        if project_id is None:
            self.ax_gantt.clear()
            self.ax_bar.clear()
            self.canvas.draw_idle()
            return
        tasks = self.db.list_tasks(project_id=project_id)

        # Gantt
        gantt_tasks = [t for t in tasks if t.start and t.end]
        self.ax_gantt.clear()
        if gantt_tasks:
            names = [t.title for t in gantt_tasks]
            starts = [date2num(datetime.datetime.fromisoformat(t.start)) for t in gantt_tasks]
            ends = [date2num(datetime.datetime.fromisoformat(t.end)) for t in gantt_tasks]
            durations = [e - s for s, e in zip(starts, ends)]
            y_pos = range(len(names))
            self.ax_gantt.barh(y_pos, durations, left=starts)
            self.ax_gantt.set_yticks(list(y_pos))
            self.ax_gantt.set_yticklabels(names)
            self.ax_gantt.set_xlabel("Date")
            self.ax_gantt.set_title("Gantt - tâches planifiées")
            self.fig.autofmt_xdate()
        else:
            self.ax_gantt.text(0.5, 0.5, "Aucune tâche avec date de début/fin", ha="center")
            self.ax_gantt.set_axis_off()

        # Remaining work
        self.ax_bar.clear()
        total_est = sum(t.estimate_hours for t in tasks)
        total_done = sum(t.done_hours for t in tasks)
        remaining = max(0.0, total_est - total_done)
        statuses = ["Fait", "Reste"]
        amounts = [total_done, remaining]
        self.ax_bar.barh(statuses, amounts)
        self.ax_bar.set_xlabel("Heures")
        self.ax_bar.set_title(f"Reste à faire: {remaining:.1f} h (Est: {total_est:.1f} h)")

        self.canvas.draw_idle()

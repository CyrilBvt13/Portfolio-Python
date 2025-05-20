# pip install flet pystray pillow

import flet as ft
from threading import Thread
from pystray import Icon, Menu, MenuItem
from PIL import Image
import io
import sys
import os
import asyncio
import subprocess
import json

TASKS_FILE = "tasks.json"

def main(page: ft.Page):
    """
    Initialise et affiche l'interface de la to-do list avec Flet.

    Args:
        page (ft.Page): L'objet Page de Flet utilisé pour construire l'interface.
    """
    page.title = "To-Do List"
    page.window.width = 400
    page.window.height = 600
    page.window.resizable = False

    tasks = ft.Column(
        width=400,
        scroll="auto"
        )  # Liste des tâches avec défilement

    def load_tasks():
        """Charge les tâches sauvegardées depuis le fichier JSON."""
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def save_tasks():
        """Sauvegarde les tâches actuelles dans un fichier JSON."""
        try:
            current = [row.controls[0].label for row in tasks.controls]
            with open(TASKS_FILE, "w", encoding="utf-8") as f:
                json.dump(current, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Erreur lors de la sauvegarde :", e)

    def add_task(e):
        """Ajoute une nouvelle tâche à la liste et la sauvegarde."""
        if new_task.value.strip():
            task = ft.Checkbox(
                label=new_task.value,
                expand=True,
                label_style=ft.TextStyle(overflow=ft.TextOverflow.ELLIPSIS)
            )
            delete_btn = ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, t=task, b=None: remove_task(t, b))
            row = ft.Row([task, delete_btn], alignment="spaceBetween")
            tasks.controls.append(row)
            new_task.value = ""
            save_tasks()
            page.update()

    def remove_task(task_cb, button):
        """Supprime une tâche de la liste et met à jour le fichier de sauvegarde."""
        tasks.controls = [row for row in tasks.controls if task_cb not in row.controls]
        save_tasks()
        page.update()

    new_task = ft.TextField(hint_text="Nouvelle tâche", on_submit=add_task, expand=True)
    add_button = ft.ElevatedButton("Ajouter", on_click=add_task)

    # Charger les tâches existantes
    for label in load_tasks():
        task = ft.Checkbox(
            label=label,
            expand=True,
            label_style=ft.TextStyle(overflow=ft.TextOverflow.ELLIPSIS)
        )
        delete_btn = ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, t=task, b=None: remove_task(t, b))
        row = ft.Row([task, delete_btn], alignment="spaceBetween")
        tasks.controls.append(row)

    page.add(
        ft.Column([
            tasks,
            ft.Row([new_task, add_button])
        ], expand=True)
    )

def setup_tray():
    """
    Configure et lance l'icône système Windows avec un menu contextuel.
    """
    with open("icon.png", "rb") as f:
        icon_image = Image.open(io.BytesIO(f.read()))

    def show_app(icon, item):
        global flet_process
        if flet_process is None or flet_process.poll() is not None:
            flet_process = subprocess.Popen([sys.executable, __file__, "--gui"])

    def quit_all(icon, item):
        os._exit(0)

    icon = Icon("To-Do", icon_image, menu=Menu(
        MenuItem("Afficher", show_app),
        MenuItem("Quitter", quit_all)
    ))
    icon.run()


def launch_app():
    """
    Lance l'application Flet dans une boucle asyncio isolée.
    """
    try:
        ft.app(target=main)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.stop()
            else:
                loop.close()
        except Exception:
            pass
        sys.exit(0)


if __name__ == "__main__":
    if "--gui" in sys.argv:
        launch_app()
    else:
        # Lance immédiatement l'interface au démarrage
        global flet_process
        flet_process = subprocess.Popen([sys.executable, __file__, "--gui"])

        # Puis lance le systray
        tray_thread = Thread(target=setup_tray, daemon=False)
        tray_thread.start()
        tray_thread.join()


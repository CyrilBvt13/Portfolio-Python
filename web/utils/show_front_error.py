import flet as ft

# Gestionnaire d'erreurs pour Flet
def show_error(page, message):
    """
    Affiche une boîte de dialogue d'erreur dans l'application Flet.
    """

    def handle_close(e):
        page.close(error_dialog)
        error_dialog.open = False

        page.update()

    error_dialog = ft.AlertDialog(
        title=ft.Text("Erreur"),
        content=ft.Text(message, text_align=ft.TextAlign.CENTER),
        actions=[ft.TextButton("OK", on_click=lambda e: handle_close(e))],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.overlay.append(error_dialog)
    error_dialog.open = True

    page.update()
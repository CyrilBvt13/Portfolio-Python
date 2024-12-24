import flet as ft

def create_file_name():
    filename_button = ft.TextButton(
        text=ft.Text(
            '', 
            weight=ft.FontWeight.BOLD
            ), 
        style=ft.ButtonStyle(
            #color=ft.colors.BLACK,
            overlay_color={"hovered": None},  # Supprime la couleur au survol
        ),
        visible=False)
    close_icon = ft.IconButton(ft.icons.CLOSE, visible=False)
    
    filename_container = ft.Row(
            controls=[
                filename_button,
                close_icon,
            ],
        ),
    
    return filename_container, filename_button, close_icon
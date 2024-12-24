import flet as ft

def create_file_name():
    filename_text = ft.Text('', weight=ft.FontWeight.BOLD)
    close_icon = ft.IconButton(ft.icons.CLOSE, visible=False)
    
    filename_container = ft.Row(
            controls=[
                filename_text,
                close_icon,
            ],
        ),
    
    return filename_container, filename_text, close_icon
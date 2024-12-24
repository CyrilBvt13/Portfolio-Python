import flet as ft
from server import start_tcp_server

def view_tcp_istening(page, dicom_dataset, scrollable_container, field_mapping, save_file_button):

    #TextField pour le host
    host_field = ft.TextField(
        'Serveur',
    )
    
    #TextField pour le port d'écoute
    port_field = ft.TextField(
        'Port d\'écoute',
    )
    
    #TextButton pour démarrer l'écoute
    start_server_button = ft.TextButton(
        text="Ecoute TCP/IP",
        on_click=lambda _: start_tcp_server(page, dicom_dataset, scrollable_container, field_mapping, save_file_button, host_field.value, port_field.value),
    )
    
    return ft.Column(
        controls=[
            start_server_button,
        ]
    )
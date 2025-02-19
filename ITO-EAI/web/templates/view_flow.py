import flet as ft
from web.utils.show_front_error import show_error

import requests
import json

class FlowContainer(ft.Column):
    """
        Classe pour la gestion/l'affichage des flux dans la Supervision

        Fonctions:
            - toggle_active_status : permet le démarrage/l'arrêt du flux
    
        Retourne :
            - Un container pour l'affichage du flux
    """
    def __init__(self, flow_id, flow_name, flow_is_active, update_page_callback):
        """
        Initialise l'affichage de la ligne du flux 

        Paramètres :
            flow_id : l'identifiant unique du flux
            flow_name : le nom du flux
            flow_is_active : un booleen définissant si le flux est actif ou non
            update_page_callback : le callback appelé lors de la modification du flux
        """
        self.flow_id = flow_id
        self.flow_is_active = flow_is_active
        self.update_page_callback = update_page_callback
        
        self.play_button = ft.IconButton(
            icon=ft.Icons.PLAY_ARROW if not flow_is_active else ft.Icons.PAUSE,
            icon_color="grey700",
            on_click=self.toggle_active_status
        )

        super().__init__(
            controls=[
                ft.Divider(),
                ft.Row(
                    controls=[
                        self.play_button,
                        ft.Icon(name=ft.Icons.CHECK_CIRCLE, color="green"),
                        ft.Text(flow_name),
                        ft.Container(expand=1),
                        ft.Icon(name=ft.Icons.EDIT, color="grey700"),
                        ft.Icon(name=ft.Icons.DELETE, color="grey700"),
                    ]
                )
            ]
        )

    def toggle_active_status(self, e):
        # D'abord activation du service puis si c'est ok alors :

        BASE = "http://127.0.0.1:5000/" 
        response = requests.get(BASE + "flow/" + self.flow_id, json={})
        current_status = response.json()[0].get('flow_is_active')
       
        new_status = not current_status

        data = response.json()
        data[0]['flow_is_active'] = not data[0]['flow_is_active']

        response = requests.post(BASE + "flow/" + self.flow_id, json=data[0])
        
        self.flow_is_active = new_status
        self.play_button.icon = ft.Icons.PLAY_ARROW if not new_status else ft.Icons.PAUSE
        self.update_page_callback()

        # + modification du statut du flux (coche verte)
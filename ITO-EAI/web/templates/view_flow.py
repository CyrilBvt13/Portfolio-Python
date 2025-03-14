import flet as ft
import requests
import json
from utils.hl7.hl7_flow import start_flow, stop_flow  # Import des fonctions de gestion des flux

BASE = "http://127.0.0.1:5000/" 

class FlowContainer(ft.Column):
    """
        Classe pour la gestion/l'affichage des flux dans la Supervision

        Fonctions:
            - toggle_active_status : permet le démarrage/l'arrêt du flux
    
        Retourne :
            - Un container pour l'affichage du flux
    """
    def __init__(self, flow_id, flow_name, flow_is_active, update_page_callback, fetch_flows_callback):
        """
        Initialise l'affichage de la ligne du flux 

        Paramètres :
            flow_id : l'identifiant unique du flux
            flow_name : le nom du flux
            flow_is_active : un booléen définissant si le flux est actif ou non
            update_page_callback : le callback appelé lors de la modification du flux
        """
        self.flow_id = flow_id
        self.flow_is_active = flow_is_active
        self.update_page_callback = update_page_callback
        self.fetch_flows_callback = fetch_flows_callback
        
        # Bouton démarrer/arrêter le flux
        self.play_button = ft.IconButton(
            icon=ft.Icons.PLAY_ARROW if not flow_is_active else ft.Icons.PAUSE,
            icon_color="grey700",
            on_click=self.toggle_active_status
        )

        # Icône de statut (rouge = inactif, vert = actif)
        self.status_icon = ft.Icon(
            name=ft.Icons.CHECK_CIRCLE  if flow_is_active else ft.Icons.CANCEL,
            color="red" if not flow_is_active else "green"
        )

        # Bouton supprimer le flux
        self.delete_button = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_color="grey700",
            on_click=self.delete_flux
        )

        super().__init__(
            controls=[
                ft.Divider(),
                ft.Row(
                    controls=[
                        self.play_button,
                        self.status_icon,
                        ft.Text(flow_name),
                        ft.Container(expand=1),
                        ft.Icon(name=ft.Icons.EDIT, color="grey700"),
                        self.delete_button,
                    ]
                )
            ]
        )

    def toggle_active_status(self, e):
        """Démarre ou arrête un flux et met à jour l'UI."""
        response = requests.get(BASE + "flow/" + self.flow_id, json={})
        current_status = response.json()[0].get('flow_is_active')
       
        new_status = not current_status
        data = response.json()
        data[0]['flow_is_active'] = new_status

        # Mise à jour du statut dans la base de données
        response = requests.post(BASE + "flow/" + self.flow_id, json=data[0])

        if new_status:
            start_flow(self.flow_id, 6000, '127.0.0.1', 6001)  # + Récupèrer les infos en bd
        else:
            stop_flow(self.flow_id)   

        # Mise à jour de l'UI
        self.flow_is_active = new_status
        self.play_button.icon = ft.Icons.PLAY_ARROW if not new_status else ft.Icons.PAUSE
        self.update_status()
        self.update_page_callback()

    def update_status(self):
        """Met à jour l'icône du statut en fonction de l'état du flux."""
        self.status_icon.name = ft.Icons.CHECK_CIRCLE  if self.flow_is_active else ft.Icons.CANCEL
        self.status_icon.color = "green" if self.flow_is_active else "red"
        self.update()  

    def update_flux(self, e):
        """Modifier le flux"""
        pass

    def delete_flux(self, e):
        """Supprimer le flux"""
        response = requests.delete(BASE + "flow/" + self.flow_id, json={})
        
        if response.status_code==204:
            print(f'✅ Flux {self.flow_id} supprimé avec succès')
            self.fetch_flows_callback()
        else:
            print(f'❌ Erreur lors de la suppression du flux {self.flow_id}')
        # /!\ Doit appeler fetch_flows de la supervision
import flet as ft
from web.utils.show_front_error import show_error

import requests
import json

def create_supervision(page, selected_group):

    """
        Récupère tous les flux de la table 'flow' pour un groupe sélectionné pour les afficher et permet la création de noveaux flux dans ce groupe
    
        Retourne :
            - Un container pour l'affichage des flux du groupe sélectionné
    """

    # Création d'un noveau flux

    # Affichage des flux du groupe sélectionné

    content = ft.Container(
        content = ft.Text(selected_group, color="grey600"),
        alignment=ft.alignment.center,
        expand=1,
    )

    return content
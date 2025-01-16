from turtle import left
import flet as ft
from web.utils.show_front_error import show_error

import requests
import json

def create_lateral_menu(page):
    """
    Crée un menu latéral contenant des boutons pour afficher les groupes de flux

    Paramètres :
        page (ft.Page) : Page principale de l'application.

    Propriétés :
        largeur : adaptative

    Retour :
        tuple : Un conteneur contenant les boutons d'action
    """

    # Liste initiale de boutons (vide au départ)
    group_buttons = ft.Column()      

    # Fonction pour récupérer la liste des groupes en base + les afficher
    def get_button():
        # Récupération des groupes en base
        BASE = "http://127.0.0.1:5000/" 
        response = requests.get(BASE + "groups/", json={})

        # Vérifier que la requête est réussie
        if response.status_code == 200:
            #On vide la liste des groupes
            group_buttons.controls.clear()

            data = response.json()  # Obtenir le contenu JSON de la réponse
            groups = data.get("groups", [])  # Extraire la liste des groupes
    
            # Fonction pour gérer la sélection des boutons
            def select_button(e):
                # Réinitialiser le style de tous les boutons
                for button in group_buttons.controls:

                    button.content.style=ft.TextStyle(
                            color="grey700",    
                            weight=ft.FontWeight.BOLD,
                        ),

                    button.style=ft.ButtonStyle(
                        bgcolor="white",
                        color="grey700",
                        overlay_color=ft.Colors.with_opacity(0.2, "grey300"),  # Couleur d'effet au survol
                        shape={
                            "hovered": ft.RoundedRectangleBorder(radius=5),  # Angles arrondis en mode survol
                            "pressed": ft.RoundedRectangleBorder(radius=5),
                            "focused": ft.RoundedRectangleBorder(radius=5),
                        },
                    )
        
                # Appliquer le style au bouton sélectionné
                e.control.content.style = ft.TextStyle(
                    color="grey700",
                    weight=ft.FontWeight.BOLD,
                )

                e.control.style = ft.ButtonStyle(
                    bgcolor="grey200",
                    shape=ft.RoundedRectangleBorder(radius=5),
                )

                # ---- AJOUTER L'AFFICHAGE DES FLUX DU GROUPE SELECTIONNE ----
                print('Groupe sélectionné : ', e.control.content.value)

                page.update()  # Mettre à jour la page

            # Parcourir les groupes et afficher chaque `group_name`
            for group in groups:
                group_name = group.get("group_name")  # Accéder à la clé "group_name"

                group_button = ft.TextButton(
                    content=ft.Text(
                        value=group_name,
                        style=ft.TextStyle(
                            weight=ft.FontWeight.BOLD,
                            color="grey700",
                        ),
                        text_align="start",
                        width=200,
                    ),
                    style=ft.ButtonStyle(
                        overlay_color=ft.Colors.with_opacity(0.2, "grey300"),  # Couleur d'effet au survol
                        shape={
                            "hovered": ft.RoundedRectangleBorder(radius=5),  # Angles arrondis en mode survol
                            "pressed": ft.RoundedRectangleBorder(radius=5),
                            "focused": ft.RoundedRectangleBorder(radius=5),
                        },
                    ),
                    on_click=select_button, #On affiche les flux du groupe sélectionné + on modifie son style
                )
        
                # Ajouter le bouton à la liste
                group_buttons.controls.append(group_button)

        else:
            message = f"Erreur {response.status_code} :", response.json()
            show_error(page, message)

        # Mettre à jour la page
        page.update()

    # Fonction pour gérer la création d'un nouveau groupe
    def add_button(e):

        #Fonction appelée lors de la validation
        def handle_create(group_name):
            # Fermeture de la popup
            page.close(new_group_dialog)
            new_group_dialog.open = False

            # Ajout du nouveau groupe en base
            BASE = "http://127.0.0.1:5000/" 
            response = requests.put(BASE + "groups/", json={"group_name": group_name})

            # Vérifier que la requête est réussie
            if response.status_code == 200:
                # Mettre à jour la liste des groupes
                get_button()
            else:
                message = f"Erreur {response.status_code} :", response.json()
                show_error(page, message)

        # Affichage de la popup pour créer le nouveau groupe
        nameField = ft.TextField(label="Nom du groupe")
        
        def createGroup(e):
            handle_create(nameField.value)

        new_group_dialog = ft.AlertDialog(
            content=ft.Column(
                controls=[
                    ft.Container(
                        height=10,
                    ),
                    nameField,
                    ft.Container(
                        height=10,
                    ),
                ],
                height=50,
                width=200,
            ),
            actions=[ft.TextButton("Valider", on_click=createGroup)],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Ajout de la popup à la page
        page.overlay.append(new_group_dialog)
        new_group_dialog.open = True

        page.update()   
        
    # Fonction pour modifier/supprimer un groupe





    # Récupération des groupes en bases lors de l'ouverture de l'application
    get_button()

    # Bouton "+" pour ajouter des TextButton
    add_button_control = ft.IconButton(
        icon=ft.Icons.ADD,
        icon_color="grey700",
        on_click=add_button,
        tooltip="Ajouter un nouveau groupe",
    )

    # Container avec hauteur adaptative pour le menu à gauche
    menu_container = ft.Container(
        content=ft.Column(
            controls=[
                    ft.Container(
                        height=10,
                    ),
                    group_buttons,  # Colonne contenant les boutons
                    add_button_control,  # Bouton d'ajout
                ],
                horizontal_alignment="center",
                scroll="auto", # Rend la colonne scrollable
                expand=True,
            ),
        bgcolor=ft.Colors.WHITE,  # Couleur de fond du menu
        height=(page.height -8 -45 -50), #Hauteur de la page - du menu entête (8 + 45) - du divider 
        width=250,  #A rendre adaptatif
    )

    return menu_container  # Retourner à la fois le conteneur et les boutons
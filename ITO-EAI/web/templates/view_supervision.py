import flet as ft
from web.templates.view_flow import FlowContainer
from web.utils.show_front_error import show_error

import requests
import json

import subprocess
import os

class Supervision:
    """
        La classe qui récupère tous les flux de la table 'flow' pour un groupe sélectionné pour les afficher et permet la création de noveaux flux dans ce groupe
    
        Retourne :
            - Un container pour l'affichage des flux du groupe sélectionné
    """

    def __init__(self, page, selected_group_id, selected_group_name):
        """
        Initialise le menu central pour gérer les flux d'un groupe

        Paramètres :
            page (ft.Page) : La page principale de l'application.
            selected_group : Le groupe sélectionné par l'utilisateur.
        """
        self.page = page
        self.selected_group_id = selected_group_id
        self.selected_group_name = selected_group_name
        self.flows_panel = ft.Container(
            alignment=ft.alignment.center,
            padding=30,
            expand=1,
        )
        #self.on_flow_selected_callback = None  # Callback à exécuter lors de la sélection d'un groupe    
    
    def modify_group(e, self):
        """
        Affiche une boîte de dialogue permettant de modifier le nom du groupe.
        """
        def handle_close(e):
            self.page.close(modify_group_dialog)
            modify_group_dialog.open = False

        def handle_modify(group_name):
            # Logique pour modifier le groupe
            pass

        # Affichage de la popup pour créer le nouveau groupe
        nameField = ft.TextField(
            label="Nom du groupe",
            text_size=14,
            color="grey800",
            bgcolor="white",
            border_color="grey800",
            focused_color="grey800",
            focused_border_color="grey800",
            selection_color="grey800",
            cursor_color="grey800",
            hint_style=ft.TextStyle(
                color="grey800",
            ),
            label_style=ft.TextStyle(
                color="grey800",
            ),
        )
        
        def modifyGroup(e):
            # Modifier le nom du groupe à partir d'une pop-up
            handle_modify(nameField.value)

        modify_group_dialog = ft.AlertDialog(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text("Modifier le groupe", expand=True),
                                ft.IconButton(icon=ft.Icons.CLOSE, icon_color="grey800", on_click=handle_close),
                            ],
                        ),
                        ft.Divider(),
                        nameField,
                        ft.Container(height=20),
                    ],
                    width=300,
                    height=140,
                ),
                actions=[
                    ft.FilledButton(
                        "Annuler", 
                        height=40,
                        width=145,
                        on_click=handle_close,
                        style=ft.ButtonStyle(
                            color="grey800",
                            bgcolor="grey300",
                            shape=ft.RoundedRectangleBorder(radius=5),
                        ),
                    ),
                    ft.OutlinedButton(
                        "Valider", 
                        height=40,
                        width=145,
                        on_click=modifyGroup,
                        style=ft.ButtonStyle(
                            color="grey800",
                            bgcolor="grey100",
                            shape=ft.RoundedRectangleBorder(radius=5),
                        ),
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.CENTER,
                shape=ft.RoundedRectangleBorder(radius=10)
            )

        # Ajout de la popup à la page
        self.page.overlay.append(modify_group_dialog)
        modify_group_dialog.open = True
        self.page.update()

    def suppress_group(self):
        """
        Affiche une boîte de dialogue permettant la suppression du groupe.
        """
        pass

    def create_supervision(self):
        """
        Crée l'interface utilisateur pour afficher les flux et gérer leur création.
        """
        selected_group_id = self.selected_group_id
        
        def add_flux(self):
        # Fonction pour gérer la création d'un nouveau flux

            def handle_close(e):
                self.page.close(new_flow_dialog)
                new_flow_dialog.open = False
            
            def handle_create(flow_name):
            #Fonction appelée lors de la validation
                self.page.close(new_flow_dialog)
                new_flow_dialog.open = False

                # Ajout du nouveau flux en base
                BASE = "http://127.0.0.1:5000/"
                response = requests.put(BASE + "flow/", json={"flow_name": flow_name, "flow_group_id": selected_group_id})

                if response.status_code == 200:
                    flow_id = response.json().get('flow_id')
                    try:
                        # Création du service Windows
                        #subprocess.run(["python", "services/service_manager.py", "install", str(flow_id)])
                        pass
                    except:
                        print('une erreur est survenue lors de la création du service')

                    fetch_flows()
                else:
                    message = f"Erreur {response.status_code} : {response.json()}"
                    show_error(self.page, message)

            # Affichage de la popup pour créer le nouveau flux
            nameField = ft.TextField(
                label="Nom du flux",
                text_size=14,
                color="grey800",
                bgcolor="white",
                border_color="grey800",
                focused_color="grey800",
                focused_border_color="grey800",
                selection_color="grey800",
                cursor_color="grey800",
                hint_style=ft.TextStyle(
                    color="grey800",
                ),
                label_style=ft.TextStyle(
                    color="grey800",
                ),
            )

            # <--------------- A FAIRE : Ajouter les autres widgets pour la création d'un nouveau flux -------------->
        
            def createFlux(e):
                handle_create(nameField.value)

            new_flow_dialog = ft.AlertDialog(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text("Créer un nouveau flux", expand=True),
                                ft.IconButton(icon=ft.Icons.CLOSE, icon_color="grey800", on_click=handle_close),
                            ],
                        ),
                        ft.Divider(),
                        nameField,
                        ft.Container(height=20),
                    ],
                    width=300,
                    height=140,
                ),
                actions=[
                    ft.FilledButton(
                        "Annuler", 
                        height=40,
                        width=145,
                        on_click=handle_close,
                        style=ft.ButtonStyle(color="grey800", bgcolor="grey300", shape=ft.RoundedRectangleBorder(radius=5)),
                    ),
                    ft.OutlinedButton(
                        "Valider", 
                        height=40,
                        width=145,
                        on_click=createFlux,
                        style=ft.ButtonStyle(color="grey800", bgcolor="grey100", shape=ft.RoundedRectangleBorder(radius=5)),
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.CENTER,
                shape=ft.RoundedRectangleBorder(radius=10)
            )

            # Ajout de la popup à la page
            self.page.overlay.append(new_flow_dialog)
            new_flow_dialog.open = True

            self.page.update()

        # Layout de la page
        flow_list_view = ft.ListView(expand=True, spacing=10)

        scrollable_container = ft.Container(content=flow_list_view, expand=True, border_radius=10, padding=10, bgcolor="white")

        content = ft.Column(
            controls=[
                ft.Row( #la ligne d'entête avec bouttons pour modifier/supprimer le groupe
                    controls=[
                        ft.Text(
                            self.selected_group_name,
                            color="grey700",
                            size=16,
                            weight="bold",
                        ),
                        ft.Container(
                            width=5,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            icon_color="grey700",
                            tooltip="Modifier le groupe",
                            on_click=self.modify_group,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color="grey700",
                            tooltip="Supprimer le groupe",
                            #on_click=suppress_group,
                        ),
                        ft.Container(
                            expand=1,
                        ),
                        ft.ElevatedButton(
                            content=ft.Container(
                                content=ft.Text("Nouveau flux"),
                                padding=10,
                            ),
                            on_click=add_flux,
                            style=ft.ButtonStyle(
                                color="white",
                                bgcolor="blue700",
                                shape=ft.RoundedRectangleBorder(radius=5),
                            ),
                        ),
                    ],
                ),
                ft.Container(
                    height=20,
                ),
                scrollable_container,
            ],
        )
        
        def fetch_flows():
            """
            Récupère les flux depuis l'API et met à jour le menu central.
            """
            BASE = "http://127.0.0.1:5000/"
            response = requests.get(BASE + "flows/" + self.selected_group_id, json={})

            if response.status_code == 200:
                flow_list_view.controls.clear()  # On vide la liste des boutons existants

                data = response.json()
                flows = data.get("flows", [])

                for flow in flows:
                    flow_name = flow.get("flow_name", "")
                    flow_id = flow.get("flow_id", "")
                    flow_is_active = flow.get("flow_is_active", False)

                    flow_list_view.controls.append(
                        FlowContainer(flow_id, flow_name, flow_is_active, self.page.update)
                    )

            elif response.status_code == 404:
                flow_list_view.controls.clear()
                flow_list_view.controls.append(
                    ft.Container(
                        content=ft.Text(
                            "Oups, il semblerait qu'il n'y ait pas encore de flux dans ce groupe!",
                            color="grey600",
                        ),
                        alignment=ft.alignment.center,
                        expand=1,
                    )
                )

            else:
                message = f"Erreur {response.status_code} : {response.json()}"
                show_error(self.page, message)

            self.page.update()

        fetch_flows()
        self.flows_panel.content=content
        return self.flows_panel
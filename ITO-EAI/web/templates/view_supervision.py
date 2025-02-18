import flet as ft
from web.utils.show_front_error import show_error

import requests
import json

import flet as ft
from web.utils.show_front_error import show_error

import requests
import json

class FlowContainer(ft.Column):
    def __init__(self, flow_id, flow_name, flow_is_active, update_page_callback):
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

class Supervision:
    """
        Récupère tous les flux de la table 'flow' pour un groupe sélectionné pour les afficher et permet la création de noveaux flux dans ce groupe
    
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
        def handle_close(e):
            self.page.close(modify_group_dialog)
            modify_group_dialog.open = False

        #Fonction appelée lors de la validation
        def handle_modify(group_name):
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

        #Pop-up pour modifier le groupe
        modify_group_dialog = ft.AlertDialog(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(
                                    "Modifier le groupe",
                                    expand=True,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    icon_color="grey800",
                                    on_click=handle_close,
                                ),
                            ],
                        ),
                        ft.Divider(),
                        nameField,
                        ft.Container(
                            height=20,
                        ),
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
        # Pop-up 'êtes vous sur?' puis retour à 'sélectionnez un groupe'
        pass

    def create_supervision(self):
        selected_group_id = self.selected_group_id

        # Fonction pour gérer la création d'un nouveau flux
        def add_flux(self):

            #Fonction pour fermer la popup
            def handle_close(e):
                self.page.close(new_flow_dialog)
                new_flow_dialog.open = False

            #Fonction appelée lors de la validation
            def handle_create(flow_name):
                # Fermeture de la popup
                self.page.close(new_flow_dialog)
                new_flow_dialog.open = False

                # Ajout du nouveau flux en base
                BASE = "http://127.0.0.1:5000/" 
                response = requests.put(BASE + "flow/", json={"flow_name": flow_name, "flow_group_id": selected_group_id})

                # Vérifier que la requête est réussie
                if response.status_code == 200:
                    # Mettre à jour la liste des groupes
                    fetch_flows()
                else:
                    message = f"Erreur {response.status_code} :", response.json()
                    show_error(self.page, message)

            # Affichage de la popup pour créer le nouveau groupe
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

            # ... Ajouter les autres widgets pour la création d'un nouveau flux
        
            def createFlux(e):
                handle_create(nameField.value)

            new_flow_dialog = ft.AlertDialog(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(
                                    "Créer un nouveau flux",
                                    expand=True,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    icon_color="grey800",
                                    on_click=handle_close,
                                ),
                            ],
                        ),
                        ft.Divider(),
                        nameField,
                        ft.Container(
                            height=20,
                        ),
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
                        on_click=createFlux,
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
            self.page.overlay.append(new_flow_dialog)
            new_flow_dialog.open = True

            self.page.update()

        # Layout de la page
        flow_list_view = ft.ListView(expand=True, spacing=10)

        scrollable_container = ft.Container(
            content=flow_list_view,
            expand=True,
            border_radius=10,
            padding=10,
            bgcolor="white",
        )

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
            Récupère les flux depuis l'API et met à jour le menu central
            """
            BASE = "http://127.0.0.1:5000/"
            response = requests.get(BASE + "flows/" + self.selected_group_id, json={})

            if response.status_code == 200:
                #self.flow_buttons.controls.clear()  # On vide la liste des boutons existants

                data = response.json()
                flows = data.get("flows", [])
      
                # Parcourir les groupes et créer des boutons pour chacun
                for flow in flows:
                    flow_name = flow.get("flow_name", "")
                    flow_id = flow.get("flow_id", "")
                    flow_is_active = flow.get("flow_is_active", False)

                    flow_list_view.controls.append(FlowContainer(flow_id, flow_name, flow_is_active, self.page.update))

            elif response.status_code == 404:
                content.controls.append(
                    ft.Container(
                        content=ft.Text("Oups il semblerait qu'il n'y ait pas encore de flux dans ce groupe!", color="grey600"),
                        alignment=ft.alignment.center,
                        expand=1,
                    ),
                )

            else:
                message = f"Erreur {response.status_code} : {response.json()}"
                show_error(self.page, message)

            self.page.update

        fetch_flows()

        self.flows_panel.content=content

        return self.flows_panel
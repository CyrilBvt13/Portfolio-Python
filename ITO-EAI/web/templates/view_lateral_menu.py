import flet as ft
import requests
from web.utils.show_front_error import show_error  # Importer la gestion des erreurs

class LateralMenu:
    def __init__(self, page):
        """
        Initialise le menu latéral pour gérer les groupes.

        Paramètres :
            page (ft.Page) : La page principale de l'application.
        """
        self.page = page
        self.selected_group_id = None
        self.selected_group_name = None
        self.group_buttons = ft.Column()
        self.on_group_selected_callback = None  # Callback à exécuter lors de la sélection d'un groupe

    def set_on_group_selected_callback(self, callback):
        """
        Enregistre une fonction à appeler lorsque le groupe sélectionné change.

        Paramètres :
            callback (function) : La fonction à appeler.
        """
        self.on_group_selected_callback = callback

    def get_selected_group(self):
        """
        Retourne le groupe actuellement sélectionné.

        Retour :
            tuple : (group_id, group_name)
        """
        return self.selected_group_id, self.selected_group_name

    def create_menu(self):
        """
        Crée le menu latéral contenant les groupes.

        Retour :
            ft.Container : Le conteneur du menu latéral.
        """

        def fetch_groups():
            """
            Récupère les groupes depuis l'API et met à jour le menu latéral.
            """
            BASE = "http://127.0.0.1:5000/"
            response = requests.get(BASE + "groups/", json={})

            if response.status_code == 200:
                self.group_buttons.controls.clear()  # On vide la liste des boutons existants

                data = response.json()
                groups = data.get("groups", [])

                # Parcourir les groupes et créer des boutons pour chacun
                for group in groups:
                    group_name = group.get("group_name", "")
                    group_id = group.get("group_id", "")

                    # Créer un bouton pour chaque groupe
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
                            overlay_color=ft.Colors.with_opacity(0.2, "grey300"),
                            padding=15,
                            shape={"hovered": ft.RoundedRectangleBorder(radius=10)},
                        ),
                        on_click=lambda e, group_id=group_id, group_name=group_name: select_button(e, group_id, group_name),
                    )

                    self.group_buttons.controls.append(group_button)

                self.page.update()
            else:
                message = f"Erreur {response.status_code} : {response.json()}"
                show_error(self.page, message)

        def select_button(e, group_id, group_name):
            """
            Gère la sélection d'un bouton de groupe.

            Paramètres :
                e : L'événement déclenché par le clic.
                group_id (str) : L'identifiant du groupe sélectionné.
                group_name (str) : Le nom du groupe sélectionné.
            """
            self.selected_group_id = group_id
            self.selected_group_name = group_name

            # Réinitialiser le style de tous les boutons
            for button in self.group_buttons.controls:
                button.content.style = ft.TextStyle(
                    color="grey700",
                    weight=ft.FontWeight.BOLD,
                )
                button.style = ft.ButtonStyle(
                    bgcolor="white",
                    color="grey700",
                    overlay_color=ft.Colors.with_opacity(0.2, "grey300"),
                    padding=15,
                    shape={"hovered": ft.RoundedRectangleBorder(radius=10)},
                )

            # Appliquer le style au bouton sélectionné
            e.control.content.style = ft.TextStyle(
                color="grey700",
                weight=ft.FontWeight.BOLD,
            )
            e.control.style = ft.ButtonStyle(
                bgcolor="grey200",
                padding=15,
                shape=ft.RoundedRectangleBorder(radius=10),
            )

            # Appeler le callback avec group_id si défini
            if self.on_group_selected_callback:
                self.on_group_selected_callback(group_id)

            self.page.update()

        # Fonction pour gérer la création d'un nouveau groupe
        def add_button(self):

            #Fonction appelée lors de la validation
            def handle_create(group_name):
                # Fermeture de la popup
                self.page.close(new_group_dialog)
                new_group_dialog.open = False

                # Ajout du nouveau groupe en base
                BASE = "http://127.0.0.1:5000/" 
                response = requests.put(BASE + "groups/", json={"group_name": group_name})

                # Vérifier que la requête est réussie
                if response.status_code == 200:
                    # Mettre à jour la liste des groupes
                    fetch_groups()
                else:
                    message = f"Erreur {response.status_code} :", response.json()
                    show_error(self.page, message)

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
            self.page.overlay.append(new_group_dialog)
            new_group_dialog.open = True

            self.page.update()   
        
        # Fonction pour modifier/supprimer un groupe




        # Charger les groupes depuis l'API
        fetch_groups()

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
                        self.group_buttons,  # Colonne contenant les boutons
                        add_button_control,  # Bouton d'ajout
                    ],
                    horizontal_alignment="center",
                    scroll="auto", # Rend la colonne scrollable
                    expand=True,
                ),
            bgcolor=ft.Colors.WHITE,  # Couleur de fond du menu
            height=(self.page.height -8 -45 -50), #Hauteur de la page - du menu entête (8 + 45) - du divider 
            width=250,  #A rendre adaptatif
        )

        return menu_container  # Retourner à la fois le conteneur et les boutons

'''

class LateralMenu:
    def __init__(self, page):
        """
        Initialise le menu latéral pour gérer les groupes.

        Paramètres :
            page (ft.Page) : La page principale de l'application.
        """
        self.page = page
        self.selected_group_id = None
        self.selected_group_name = None
        self.group_buttons = ft.Column()
        self.on_group_selected_callback = None  # Callback à exécuter lors de la sélection d'un groupe

    def set_on_group_selected_callback(self, callback):
        """
        Enregistre une fonction à appeler lorsque le groupe sélectionné change.

        Paramètres :
            callback (function) : La fonction à appeler.
        """
        self.on_group_selected_callback = callback

    def get_selected_group(self):
        """
        Retourne le groupe actuellement sélectionné.

        Retour :
            str : Nom du groupe sélectionné.
        """
        return self.selected_group_id, self.selected_group_name

    def create_menu(self):
        """
        Crée le menu latéral contenant les groupes.

        Retour :
            ft.Container : Le conteneur du menu latéral.
        """

        def fetch_groups():
            """
            Récupère les groupes depuis l'API et met à jour le menu latéral.
            """
            BASE = "http://127.0.0.1:5000/"
            response = requests.get(BASE + "groups/", json={})

            if response.status_code == 200:
                self.group_buttons.controls.clear()  # On vide la liste des boutons existants

                data = response.json()
                groups = data.get("groups", [])

                # Parcourir les groupes et créer des boutons pour chacun
                for group in groups:
                    group_name = group.get("group_name", "")
                    group_id = group.get("group_id", "")

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
                            overlay_color=ft.Colors.with_opacity(0.2, "grey300"),
                            padding=15,
                            shape={"hovered": ft.RoundedRectangleBorder(radius=10)},
                        ),
                        on_click=select_button,
                    )

                    self.group_buttons.controls.append(group_button)

                self.page.update()
            else:
                message = f"Erreur {response.status_code} : {response.json()}"
                show_error(self.page, message)

        def select_button(e):
            """
            Gère la sélection d'un bouton de groupe.
            """
            self.selected_group = e.control.content.value

            # Réinitialiser le style de tous les boutons
            for button in self.group_buttons.controls:
                button.content.style = ft.TextStyle(
                    color="grey700",
                    weight=ft.FontWeight.BOLD,
                )
                button.style = ft.ButtonStyle(
                    bgcolor="white",
                    color="grey700",
                    overlay_color=ft.Colors.with_opacity(0.2, "grey300"),
                    padding=15,
                    shape={"hovered": ft.RoundedRectangleBorder(radius=10)},
                )

            # Appliquer le style au bouton sélectionné
            e.control.content.style = ft.TextStyle(
                color="grey700",
                weight=ft.FontWeight.BOLD,
            )
            e.control.style = ft.ButtonStyle(
                bgcolor="grey200",
                padding=15,
                shape=ft.RoundedRectangleBorder(radius=10),
            )

            # Appeler le callback si défini
            if self.on_group_selected_callback:
                self.on_group_selected_callback()

            self.page.update()
'''
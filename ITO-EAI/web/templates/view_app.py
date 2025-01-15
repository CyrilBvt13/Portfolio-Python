from calendar import c
from stringprep import c22_specials
import flet as ft
from flet.core.border_radius import horizontal
from web.templates.view_top_menu import create_menu
from web.templates.view_lateral_menu import create_lateral_menu

from web.utils.show_front_error import show_error  # Importer la gestion des erreurs

def AppView(page):
    """
    Crée l'interface utilisateur principale de l'application.

    Paramètres :
        page (ft.Page) : Page principale de l'application.

    Retour :
        ft.Container : Conteneur contenant les composants de l'application.
    """

    '''# Exemple : Bouton qui déclenche une requête vers Flask
    def on_test_click(e):
        """
        Tente de se connecter au backend Flask pour un test.
        Capture les erreurs HTTP et affiche une boîte de dialogue en cas d'erreur.
        """
        try:
            import requests
            response = requests.get("http://127.0.0.1:5000/test")
            if response.status_code == 200:
                page.snack_bar = ft.SnackBar(ft.Text("Succès : " + response.json()["message"]))
                page.snack_bar.open = True
            else:
                show_error(page, f"Erreur HTTP : {response.status_code} - {response.json()['error']}")
        except Exception as e:
            show_error(page, f"Impossible de se connecter au backend Flask : {str(e)}")'''

    # Menu entête
    menu, notification_button, disconnect_button = create_menu(page)

    # Séparateur horizontal
    horizontal_divider = ft.Divider(
        height=2, 
        color="grey400",
    )

    # Menu latéral
    lateral_menu = create_lateral_menu(page)

    # Corps de l'application (menu latéral + flux) avec divider draggable
    def move_vertical_divider(e: ft.DragUpdateEvent):
        if (e.delta_x > 0 and lateral_menu.width < 400) or (e.delta_x < 0 and lateral_menu.width > 200):
            lateral_menu.width += e.delta_x
        lateral_menu.update()

    def show_draggable_cursor(e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        e.control.update()

    body =  ft.Container(
        content=ft.Row(
            controls=[
                lateral_menu,
                ft.GestureDetector(
                    content=ft.VerticalDivider(),
                    drag_interval=10,
                    on_pan_update=move_vertical_divider,
                    on_hover=show_draggable_cursor,
                ),
                ft.Container(
                    #width=(page.width-lateral_menu.width-16), #1 = la largeur du VerticalDivider
                    alignment=ft.alignment.center,
                    expand=1,
                    bgcolor=ft.Colors.GREY,
                ),
            ],
            spacing=0,
        ),
        width=page.width,
        height=(page.height - menu.height),
    )

    # Conteneur principal structurant l'interface utilisateur
    content = ft.Container(
        content=ft.Column(
                    controls=[
                        menu, #Le menu entête
                        horizontal_divider, #divider
                        body, #corps = menu latéral + vue des flux
                    ],
                    alignment="center",
                    horizontal_alignment="center",
                ),
        width=page.width,
        height=page.height,
        )

    # Fonction pour ajuster la taille du container lorsque la fenêtre est redimensionnée
    def on_resized(e): 
        content.width = page.width
        content.height = page.height 

        page.update() 

    # Attacher l'événement de redimensionnement à la page
    page.on_resized = on_resized

    # Retourner le conteneur principal
    return content
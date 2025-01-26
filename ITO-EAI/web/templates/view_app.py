import flet as ft
from web.templates.view_top_menu import create_menu
from web.templates.view_lateral_menu import LateralMenu
from web.templates.view_supervision import create_supervision
from web.utils.show_front_error import show_error  # Gestion des erreurs

def AppView(page):
    """
    Crée l'interface utilisateur principale de l'application.

    Paramètres :
        page (ft.Page) : Page principale de l'application.

    Retour :
        ft.Container : Conteneur contenant les composants de l'application.
    """

    # Créer le menu d'entête
    menu, notification_button, disconnect_button = create_menu(page)

    # Séparateur horizontal
    horizontal_divider = ft.Divider(
        height=2, 
        color="grey400",
    )

    # Vue des flux (conteneur dynamique)
    supervision = ft.Container(
        alignment=ft.alignment.center,
        expand=1,
        content=ft.Text("Aucun groupe sélectionné", color="grey600"),
    )

    # Créer le menu latéral
    lat_menu = LateralMenu(page)

    # Fonction pour mettre à jour la supervision en fonction du groupe sélectionné
    def update_supervision_view(group_id=None):
        """
        Met à jour la supervision en fonction du groupe sélectionné.

        Paramètres :
            group_id (str) : L'identifiant du groupe sélectionné.
        """
        if group_id:
            #print(f"Groupe sélectionné : {group_id}")
            selected_group_id, selected_group_name = lat_menu.get_selected_group()
            supervision.content = create_supervision(page, selected_group_id)

        else:
            supervision.content = ft.Text("Aucun groupe sélectionné", color="grey600")

        page.update()

    # Injecter la fonction de mise à jour dans le menu latéral
    lat_menu.set_on_group_selected_callback(update_supervision_view)

    # Corps de l'application (menu latéral + vue des flux) avec un diviseur vertical
    body = ft.Container(
        content=ft.Row(
            controls=[
                lat_menu.create_menu(),  # Le menu des groupes
                ft.VerticalDivider(
                    trailing_indent=7,
                ),
                supervision,  # La vue des flux
            ],
            spacing=0,
        ),
        width=page.width,
        height=(page.height - 8 - menu.height - 32),
    )

    # Conteneur principal structurant l'interface utilisateur
    content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(height=8),  # Espacement supérieur
                menu,  # Le menu d'entête
                horizontal_divider,  # Diviseur horizontal
                body,  # Corps = menu latéral + vue des flux
            ],
            alignment="center",
            horizontal_alignment="center",
        ),
        width=page.width,
        height=page.height,
    )

    # Fonction pour ajuster la taille du conteneur lorsque la fenêtre est redimensionnée
    def on_resized(e): 
        content.width = page.width
        content.height = page.height
        body.height = page.height - 8 - menu.height - 32
        page.update()

    # Attacher l'événement de redimensionnement à la page
    page.on_resized = on_resized

    # Initialiser la vue avec le groupe par défaut (si disponible)
    update_supervision_view()

    # Retourner le conteneur principal
    return content
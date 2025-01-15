import flet as ft

def create_menu(page):
    """
    Crée un menu en entête contenant des boutons pour afficher :
        - les notifications 
        - déconnecter l'utilisateur

    Paramètres :
        page (ft.Page) : Page principale de l'application.

    Propriétés :
        hauteur : 50 px

    Retour :
        tuple : Un conteneur contenant les boutons d'action et le boutons d'action
    """

    # Bouton pour ouvrir les notifications
    notification_button = ft.IconButton(
                    icon=ft.Icons.NOTIFICATIONS,
                    #icon=ft.Icons.NOTIFICATION_IMPORTANT,
                    icon_color="grey700",
                    #icon_color="red700",
                    tooltip="Notifications",
                    #on_click=
                )

    # Bouton pour déconnecter l'utilisateur
    disconnect_button = ft.IconButton(
                    icon=ft.Icons.LOGOUT,
                    icon_color="grey700",
                    tooltip="Déconnexion",
                    #on_click=
                )

    # Container avec hauteur adaptative pour le menu à gauche
    menu_container = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    expand=True,
                ),
                notification_button, 
                disconnect_button,
                ft.Container(
                    width=20,
                ),
            ],
        ), 
        bgcolor=ft.Colors.WHITE,  # Couleur de fond du menu
        height=60,
        width=page.width,  
    )

    return menu_container, notification_button, disconnect_button  # Retourner à la fois le conteneur et les boutons
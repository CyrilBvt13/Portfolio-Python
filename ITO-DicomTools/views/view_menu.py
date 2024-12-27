import flet as ft

def create_menu(page, file_picker, save_file_picker):
    """
    Crée un menu latéral contenant des boutons pour charger et sauvegarder des fichiers DICOM.

    Paramètres :
        page (ft.Page) : Page principale de l'application.
        file_picker (ft.FilePicker) : Composant pour la sélection des fichiers.
        save_file_picker (ft.FilePicker) : Composant pour la sauvegarde des fichiers.

    Retour :
        tuple : Un conteneur contenant les boutons d'action, le bouton de sauvegarde et le bouton d'envoi TCP/IP.
    """
    # Bouton pour ouvrir un fichier DICOM à l'aide du FilePicker
    open_icon = ft.Icon(
                    name=ft.Icons.FILE_OPEN,
                    color=ft.Colors.GREY_800,
                    size=20,
                    )

    open_text = ft.Text(
                    "Ouvrir",
                    color=ft.Colors.GREY_800,
                    text_align="start",
                    width=210,
                )

    pick_file_button = ft.TextButton(
        content=ft.Row(
            controls=[
                open_icon,
                open_text,
            ],
        ),
        on_click=lambda _: file_picker.pick_files(dialog_title="Sélectionner un fichier DICOM"),
        style=ft.ButtonStyle(
            overlay_color=ft.colors.with_opacity(0.2, ft.colors.GREY_200),  # Couleur d'effet au survol
            shape={
                "hovered": ft.RoundedRectangleBorder(radius=5),  # Angles arrondis en mode survol
                "pressed": ft.RoundedRectangleBorder(radius=5),
                "focused": ft.RoundedRectangleBorder(radius=5),
            },
        ),
    )

    # Bouton pour sauvegarder les modifications apportées au fichier DICOM
    save_icon = ft.Icon(
                    name=ft.Icons.SAVE,
                    size=20,
                    color = ft.Colors.GREY_300
                    )

    save_text = ft.Text(
                    "Sauvegarder",
                    text_align="start",
                    width=210,
                    color = ft.Colors.GREY_300
                )

    save_file_button = ft.TextButton(
        content=ft.Row(
            controls=[
                save_icon,
                save_text,
            ],
        ),
        on_click=lambda _: save_file_picker.save_file(dialog_title="Enregistrer le fichier DICOM"),
        disabled=True,  # Désactivé par défaut
        style=ft.ButtonStyle(
            overlay_color=ft.colors.with_opacity(0.2, ft.colors.GREY_200),  # Couleur d'effet au survol
            shape={
                "hovered": ft.RoundedRectangleBorder(radius=5),  # Angles arrondis en mode survol
                "pressed": ft.RoundedRectangleBorder(radius=5),
                "focused": ft.RoundedRectangleBorder(radius=5),
            },
        ),
    )

    # Bouton pour ouvrir l'interface d'écoute TCP/IP

        #--- Séparer l'icon et le text ici ---

    tcp_listen_button = ft.TextButton(
        content=ft.Row(
            controls=[
                ft.Icon(
                    name=ft.Icons.LOGIN,
                    color = ft.Colors.GREY_300,
                    size=20,
                    ),
                ft.Text(
                    "Ecoute TCP/IP",
                    color = ft.Colors.GREY_300,
                    text_align="start",
                    width=210,
                ),
            ],
        ),
        #on_click=lambda _: afficher l'interface d'écoute TCP/IP,
        disabled=True, # Désactivé par défaut
        style=ft.ButtonStyle(
            overlay_color=ft.colors.with_opacity(0.2, ft.colors.GREY_200),  # Couleur d'effet au survol
            shape={
                "hovered": ft.RoundedRectangleBorder(radius=5),  # Angles arrondis en mode survol
                "pressed": ft.RoundedRectangleBorder(radius=5),
                "focused": ft.RoundedRectangleBorder(radius=5),
            },
        ),
    )

    # Bouton pour ouvrir l'interface d'émission TCP/IP
    send_icon = ft.Icon(
                    name=ft.Icons.LOGOUT,
                    size=20,
                    color = ft.Colors.GREY_300
                    )

    send_text = ft.Text(
                    "Envoi TCP/IP",
                    text_align="start",
                    width=210,
                    color = ft.Colors.GREY_300
                )

    tcp_send_button = ft.TextButton(
        content=ft.Row(
            controls=[
                send_icon,
                send_text,
            ],
        ),
        #on_click=lambda _: afficher l'interface d'envoi TCP/IP,
        disabled=True,  # Désactivé par défaut
        style=ft.ButtonStyle(
            overlay_color=ft.colors.with_opacity(0.2, ft.colors.GREY_200),  # Couleur d'effet au survol
            shape={
                "hovered": ft.RoundedRectangleBorder(radius=5),  # Angles arrondis en mode survol
                "pressed": ft.RoundedRectangleBorder(radius=5),
                "focused": ft.RoundedRectangleBorder(radius=5),
            },
        ),
    )
    
    # Texte pour la version du programme
    version_text = ft.Text(
        'V 0.1.1',
        size=10,
    )

    # Container avec hauteur adaptative pour le menu à gauche
    menu_container = ft.Container(
        content=ft.Column(controls=[
            ft.Container(
                height=2,
                ),
            pick_file_button, 
            save_file_button,
            tcp_listen_button,
            tcp_send_button,
            ft.Container(
                expand=True,
            ),
            version_text
            ],
        ),  # Organisation verticale des boutons
        bgcolor=ft.colors.WHITE,  # Couleur de fond du menu
        height=page.height,  # Hauteur du conteneur ajustée à la page
        width=250,  # Largeur fixe du menu latéral
        padding=10,  # Espacement interne
        alignment=ft.alignment.top_left,  # Aligne les éléments en haut à gauche pour éviter tout débordement
    )

    return menu_container, save_icon, save_text, save_file_button, send_icon, send_text, tcp_send_button  # Retourner à la fois le conteneur et les boutons
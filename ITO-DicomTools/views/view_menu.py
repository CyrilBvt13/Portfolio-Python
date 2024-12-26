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
    pick_file_button = ft.TextButton(
        content=ft.Text(
            "Ouvrir",
            text_align="start",
            width=210,
        ),
        on_click=lambda _: file_picker.pick_files(dialog_title="Sélectionner un fichier DICOM"),
        style=ft.ButtonStyle(
            overlay_color=ft.colors.with_opacity(0.2, ft.colors.GREY_400),  # Couleur d'effet au survol
            shape={
                "hovered": ft.RoundedRectangleBorder(radius=5),  # Angles arrondis en mode survol
                "pressed": ft.RoundedRectangleBorder(radius=5),
                "focused": ft.RoundedRectangleBorder(radius=5),
            },
        ),
    )

    # Bouton pour sauvegarder les modifications apportées au fichier DICOM
    save_file_button = ft.TextButton(
        content=ft.Text(
            "Sauvegarder",
            text_align="start",
            width=210,
        ),
        on_click=lambda _: save_file_picker.save_file(dialog_title="Enregistrer le fichier DICOM"),
        disabled=True,  # Désactivé par défaut
        style=ft.ButtonStyle(
            overlay_color=ft.colors.with_opacity(0.2, ft.colors.GREY_400),  # Couleur d'effet au survol
            shape={
                "hovered": ft.RoundedRectangleBorder(radius=5),  # Angles arrondis en mode survol
                "pressed": ft.RoundedRectangleBorder(radius=5),
                "focused": ft.RoundedRectangleBorder(radius=5),
            },
        ),
    )
    
    # Bouton pour ouvrir l'interface d'écoute TCP/IP
    tcp_listen_button = ft.TextButton(
        content=ft.Text(
            "Ecoute TCP/IP (non dispo)",
            text_align="start",
            width=210,
        ),
        #on_click=lambda _: afficher l'interface d'écoute TCP/IP,
        disabled=True, # Désactivé par défaut
        style=ft.ButtonStyle(
            overlay_color=ft.colors.with_opacity(0.2, ft.colors.GREY_400),  # Couleur d'effet au survol
            shape={
                "hovered": ft.RoundedRectangleBorder(radius=5),  # Angles arrondis en mode survol
                "pressed": ft.RoundedRectangleBorder(radius=5),
                "focused": ft.RoundedRectangleBorder(radius=5),
            },
        ),
    )
    
    # Bouton pour ouvrir l'interface d'émission TCP/IP
    tcp_send_button = ft.TextButton(
        content=ft.Text(
            "Envoi TCP/IP",
            text_align="start",
            width=210,
        ),
        #on_click=lambda _: afficher l'interface d'envoi TCP/IP,
        disabled=True,  # Désactivé par défaut
        style=ft.ButtonStyle(
            overlay_color=ft.colors.with_opacity(0.2, ft.colors.GREY_400),  # Couleur d'effet au survol
            shape={
                "hovered": ft.RoundedRectangleBorder(radius=5),  # Angles arrondis en mode survol
                "pressed": ft.RoundedRectangleBorder(radius=5),
                "focused": ft.RoundedRectangleBorder(radius=5),
            },
        ),
    )
    
    # Texte pour la version du programme
    version_text = ft.Text(
        'V 0.1.0',
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

    return menu_container, save_file_button, tcp_send_button  # Retourner à la fois le conteneur et les boutons
import flet as ft
from server import start_tcp_server

def view_tcp_istening(page, dicom_dataset, scrollable_container, field_mapping, save_file_button):
    """
    Crée une interface utilisateur pour configurer et démarrer une écoute TCP/IP 
    afin de recevoir des fichiers DICOM.

    Paramètres :
        page (ft.Page) : Page principale de l'application, utilisée pour mettre à jour l'interface.
        dicom_dataset : Dataset DICOM chargé dans l'application.
        scrollable_container : Conteneur défilable pour afficher les balises DICOM reçues.
        field_mapping : Dictionnaire associant les champs modifiables aux éléments DICOM.
        save_file_button (ft.TextButton) : Bouton de sauvegarde à activer après réception d'un fichier.

    Retour :
        ft.Column : Une colonne contenant les champs de configuration et le bouton pour démarrer l'écoute.
    """

    # Champ de saisie pour spécifier l'adresse IP ou le nom d'hôte du serveur
    host_field = ft.TextField(
        label="Serveur",  # Libellé affiché au-dessus du champ
        hint_text="Entrez l'adresse IP ou le nom d'hôte",  # Texte d'indication
        value="0.0.0.0",  # Par défaut, écoute sur toutes les interfaces
    )

    # Champ de saisie pour spécifier le port d'écoute
    port_field = ft.TextField(
        label="Port d'écoute",  # Libellé affiché au-dessus du champ
        hint_text="Entrez le port (ex : 104)",  # Texte d'indication
        value="104",  # Port DICOM standard par défaut
    )

    # Bouton pour démarrer l'écoute du serveur TCP/IP
    start_server_button = ft.TextButton(
        text="Écoute TCP/IP",  # Texte affiché sur le bouton
        on_click=lambda _: start_tcp_server(
            page,  # Page principale pour afficher des messages ou mises à jour
            dicom_dataset,  # Dataset DICOM utilisé pour mettre à jour l'application
            scrollable_container,  # Conteneur pour afficher les données reçues
            field_mapping,  # Dictionnaire de mappage pour les champs
            save_file_button,  # Bouton de sauvegarde à activer après réception
            host_field.value,  # Adresse IP ou nom d'hôte spécifié par l'utilisateur
            port_field.value  # Port d'écoute spécifié par l'utilisateur
        ),
    )

    # Retourne une colonne contenant les champs de saisie et le bouton
    return ft.Column(
        controls=[
            host_field,  # Champ pour l'adresse IP
            port_field,  # Champ pour le port
            start_server_button,  # Bouton pour démarrer l'écoute
        ]
    )
import flet as ft
from tcp_handler import send_dicom_file
from views.view_error import show_error

def create_tcp_form(page, dicom_dataset):
    """
    Crée un formulaire pour définir l'IP, le port, l'AET et l'AEC pour l'envoi TCP/IP.

    Paramètres :
        send_button (ft.TextButton) : Bouton d'envoi qui sera activé ou désactivé en fonction de la validation du formulaire.

    Retour :
        dict : Champs du formulaire (ip_field, port_field, aet_field, aec_field) pour récupérer les valeurs saisies.
    """
    
    ip_field = ft.TextField(label="Adresse IP", hint_text="127.0.0.1", value="127.0.0.1", bgcolor=ft.colors.WHITE, width=300)
    port_field = ft.TextField(label="Port", hint_text="14090", value="14090", bgcolor=ft.colors.WHITE, width=300)
    aet_field = ft.TextField(label="AET Émetteur", hint_text="AET", value="AET", bgcolor=ft.colors.WHITE, width=300)
    aec_field = ft.TextField(label="AEC Récepteur", hint_text="AEC", value="AEC", bgcolor=ft.colors.WHITE, width=300)
    send_button = ft.TextButton('Envoyer')

    def validate_fields(_):
        # Activer ou désactiver le bouton en fonction des champs remplis
        send_button.disabled = not (ip_field.value and port_field.value.isdigit() and aet_field.value and aec_field.value)
        send_button.update()

    ip_field.on_change = validate_fields
    port_field.on_change = validate_fields
    aet_field.on_change = validate_fields
    aec_field.on_change = validate_fields
    
    def handle_send_button(_):
        """
        Gère l'action de clic sur le bouton d'envoi.
        Récupère les valeurs des champs de formulaire et appelle `send_dicom_file`.
        """
        ip = ip_field.value
        port = int(port_field.value)
        aet = aet_field.value
        aec = aec_field.value

        if dicom_dataset:  # Vérifie que le dataset DICOM est chargé
            result = send_dicom_file(dicom_dataset, ip, port, aet, aec)
            show_error(page, result)
        else:
            show_error(page, "Aucun fichier DICOM chargé pour l'envoi.")

    # Associer la fonction au bouton
    send_button.on_click = handle_send_button

    form = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    height=25,
                ),
                ip_field, 
                port_field,
                aet_field, 
                aec_field,
                ft.Container(
                    height=25,
                ),
                send_button
            ],
            horizontal_alignment="center",
        ),
        alignment=ft.alignment.center,
        height=page.height,  # Hauteur du conteneur ajustée à la page 
        width=(page.width-250),  # Largeur fixe du menu latéral = taille de la page - la barre de navigation
    )
    return form
import flet as ft
from types import NoneType
from tcp_handler import receive_dicom_file
from views.view_error import show_error

def create_tcp_listening_form(dicom_dataset, viewer_container, scrollable_container, filename_button, page, field_mapping, on_receive_callback=None):
    """
    Crée un formulaire pour définir le port et l'AET pour la réception TCP/IP.

    Paramètres :
        dicom_dataset (pydicom.dataset.FileDataset) : Dataset initial à afficher.
        viewer_container (ft.Container) : Conteneur principal pour la visualisation.
        scrollable_container (ft.Container) : Conteneur scrollable pour afficher les balises DICOM.
        filename_button (ft.TextButton) : Bouton pour afficher le nom du fichier.
        page (ft.Page) : Page principale Flet.
        field_mapping (dict) : Mapping entre les champs modifiables et les éléments DICOM.
        on_receive_callback (function) : Fonction appelée lorsque le fichier est reçu. Signature : `callback(dicom_dataset, filename)`.

    Retour :
        ft.Container : Formulaire pour la saisie des informations TCP/IP.
    """

    show_error(page, f"Cette fonctionnalité est encore en version Béta. Cela signifie que des bugs peuvent survenir, notamment une latence de l'application.")

    port_field = ft.TextField(label="Port", hint_text="14090", value="14090", bgcolor=ft.colors.WHITE, width=300)
    aet_field = ft.TextField(label="AET Émetteur", hint_text="AET", value="AET", bgcolor=ft.colors.WHITE, width=300)
    receive_button = ft.TextButton('Recevoir')

    def validate_fields(_):
        # Activer ou désactiver le bouton en fonction des champs remplis
        receive_button.disabled = not (port_field.value.isdigit() and aet_field.value)
        receive_button.update()

    port_field.on_change = validate_fields
    aet_field.on_change = validate_fields

    def handle_receive_button(_):
        """
        Gère l'action de clic sur le bouton de réception.
        Récupère les valeurs des champs de formulaire et appelle `receive_dicom_file`.
        """
        port = int(port_field.value)
        aet = aet_field.value

        try:
            # Réception du fichier DICOM
            dicom_dataset = receive_dicom_file(page, port, aet)

            # Réinitialiser le conteneur et le mapping des champs
            scrollable_container.controls.clear()
            field_mapping.clear()
            filename_button.visible = False

            # Fonction locale pour afficher les éléments du dataset
            def display_element(element, level=0, parent=None):
                """
                Fonction récursive pour afficher les balises et sous-balises DICOM et permettre leur modification.
                """
                controls = []
                indent = "    " * level  # Indentation pour les sous-niveaux

                if element.VR == "SQ":  # Gestion des séquences (balises avec sous-balises)
                    controls.append(ft.Text(value=f"{indent}{element.name} (Sequence):", weight="bold"))
                    for i, item in enumerate(element):
                        controls.append(ft.Text(value=f"{indent}  Item {i+1}:", italic=True))
                        for sub_element in item:
                            controls.extend(display_element(sub_element, level + 2, item))
                else:
                    # Ajouter l'élément et son champ modifiable à l'interface
                    tag_text = ft.Text(value=f"{indent}{element.name} [{element.tag}]:", width=350)
                    value_field = ft.TextField(value=str(element.value), multiline=True, bgcolor=ft.colors.WHITE)
                    field_mapping[value_field] = (element, parent)  # Ajouter au mapping
                    row = ft.Row([tag_text, value_field], vertical_alignment="center")
                    controls.append(row)
                return controls

            # Ajouter tous les éléments au conteneur
            for element in dicom_dataset:
                scrollable_container.controls.extend(display_element(element))

            # Ajouter le nom du fichier au champ texte
            filename = 'Fichier reçu par TCP/IP'
            filename_button.text = filename
            filename_button.visible = True

            # Afficher les changements sur la page
            viewer_container.content=scrollable_container #On réinitialise le contenu de viewer_container
            viewer_container.update()

            scrollable_container.update()
            filename_button.update()

            

            # Appeler le callback avec les données reçues
            if on_receive_callback:
                on_receive_callback(dicom_dataset, filename)

        except Exception as ex:
            # Gérer les autres erreurs
            show_error(page, f"Une erreur est survenue : {ex}")
            scrollable_container.controls.clear()
            filename_button.visible = False

    # Associer la fonction au bouton
    receive_button.on_click = handle_receive_button

    form = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    height=25,
                ),
                port_field,
                aet_field,
                ft.Container(
                    height=25,
                ),
                receive_button
            ],
            horizontal_alignment="center",
        ),
        alignment=ft.alignment.center,
        height=page.height,  # Hauteur du conteneur ajustée à la page
        width=(page.width - 250),  # Largeur fixe du menu latéral = taille de la page - la barre de navigation
    )
    return form
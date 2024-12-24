import flet as ft
import pydicom
from pydicom.errors import InvalidDicomError
from views.view_error import show_error


def process_dicom_file(e, dicom_dataset, scrollable_container, filename_button, page, field_mapping):
    """
    Traite le fichier DICOM sélectionné, met à jour l'interface utilisateur et initialise le mapping des champs.

    Paramètres :
        e : Événement de sélection de fichier.
        dicom_dataset : Dataset DICOM actuellement chargé.
        scrollable_container : Conteneur défilable pour afficher les balises DICOM.
        page : Page Flet pour mettre à jour l'interface.
        field_mapping : Dictionnaire associant les champs modifiables aux éléments du dataset.

    Retour :
        tuple : (dicom_dataset, nom_du_fichier) où :
            - dicom_dataset : Dataset DICOM chargé à partir du fichier.
            - nom_du_fichier : Nom du fichier chargé (ou `None` si aucun fichier n'est sélectionné).
    """
    
    file_path = e.files[0].path if e.files else None
    if not file_path:
        return dicom_dataset, None  # Si aucun fichier n'est sélectionné, retourner le dataset inchangé.

    file_name = e.files[0].name  # Récupérer le nom du fichier
    
    try:
        # Charger le fichier DICOM
        dicom_dataset = pydicom.dcmread(file_path)

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

        #Ajouter le nom du fichier au champs texte
        filename_button.text = file_name
        filename_button.visible = True
        
        # Afficher les changements sur la page
        scrollable_container.update()
        filename_button.update()
        
    except InvalidDicomError:
        # Gérer les erreurs DICOM invalides
        show_error(page, "Le fichier sélectionné n'est pas un fichier DICOM valide.")
        scrollable_container.controls.clear()
        filename_button.visible = False
    except Exception as ex:
        # Gérer les autres erreurs
        show_error(page, f"Une erreur est survenue : {ex}")
        scrollable_container.controls.clear()
        filename_button.visible = False

    # Retourner le dataset chargé et le nom du fichier
    return dicom_dataset, file_name

def update_dicom_dataset_from_ui(dicom_dataset, field_mapping):
    """
    Met à jour le dataset DICOM avec les valeurs modifiées dans l'interface utilisateur.

    Paramètres :
        dicom_dataset : Dataset DICOM chargé.
        field_mapping : Dictionnaire associant les champs modifiables aux éléments du dataset.

    Retour :
        dicom_dataset : Dataset DICOM mis à jour.
    """
    for textfield, (element, parent) in field_mapping.items():
        new_value = textfield.value.strip()
        if parent:
            parent[element.tag].value = new_value
        else:
            element.value = new_value
    return dicom_dataset

def save_dicom_file(e, dicom_dataset, field_mapping, page):
    """
    Sauvegarde le dataset DICOM mis à jour dans un fichier.

    Paramètres :
        e : Événement de sélection de fichier.
        dicom_dataset : Dataset DICOM à sauvegarder.
        field_mapping : Dictionnaire des champs modifiables dans l'interface utilisateur.
        page : Page Flet pour afficher les messages.
    """
    file_path = e.path if e.path else None
    if not file_path:
        return
    try:
        # Met à jour le dataset avec les valeurs de l'interface
        updated_dataset = update_dicom_dataset_from_ui(dicom_dataset, field_mapping)

        # Sauvegarde le dataset mis à jour
        updated_dataset.save_as(file_path)

        # Afficher un message de succès
        from views.view_error import show_error
        show_error(page, "Fichier DICOM sauvegardé avec succès.")
    except Exception as ex:
        from views.view_error import show_error
        show_error(page, f"Une erreur est survenue lors de la sauvegarde : {ex}")
    page.update()
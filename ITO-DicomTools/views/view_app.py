import flet as ft
from flet import Container
from views.view_error import show_error

import pydicom
from pydicom.errors import InvalidDicomError

# Fonction principale pour la création de l'interface utilisateur de l'application
def AppView(page):
    """
    Crée l'interface utilisateur pour la sélection et l'affichage d'un fichier DICOM
    Paramètres :
        page (ft.Page) : Objet représentant la page de l'application.
    Retour :
        content (ft.Container) : Conteneur contenant tous les éléments de l'interface utilisateur.
    """
    
    # Widgets de l'interface
    file_picker = ft.FilePicker()  # FilePicker pour la sélection du fichier DICOM
    save_file_picker = ft.FilePicker()  # FilePicker pour la sauvegarde du fichier DICOM
    error_message = ft.Text(color="red")  # Zone pour afficher les messages d'erreur

    # Conteneur scrollable pour les TextFields
    scrollable_container = ft.Column(scroll="always")

    # Variable pour stocker le dataset DICOM
    dicom_dataset = None  # Initialisé à None, il contiendra les données du fichier DICOM
    field_mapping = {}  # Dictionnaire pour associer chaque TextField à un élément DICOM

    # Fonction pour afficher les éléments DICOM (balises et sous-balises)
    def display_element(element, level=0, parent=None):
        """
        Fonction récursive pour afficher les balises et sous-balises DICOM et permettre leur modification
        Paramètres :
            element (pydicom.DataElement) : Élément DICOM à afficher.
            level (int) : Niveau de profondeur de l'élément dans la hiérarchie (pour l'indentation).
            parent (pydicom.DataElement, optional) : Élément parent si l'élément est une sous-balise.
        Retour :
            controls (list) : Liste des éléments de l'interface (Text et TextField).
        """
        controls = []
        indent = "    " * level  # Détermine l'indentation en fonction du niveau d'imbrication

        if element.VR == "SQ":  # Gérer les séquences (balises avec sous-balises)
            # Ajouter un titre pour la séquence
            controls.append(ft.Text(value=f"{indent}{element.name} (Sequence):", weight="bold"))
            for i, item in enumerate(element):  # Itérer sur les éléments dans la séquence
                controls.append(ft.Text(value=f"{indent}  Item {i+1}:", italic=True))
                for sub_element in item:  # Itérer sur les sous-éléments de chaque élément
                    controls.extend(display_element(sub_element, level + 2, item))
        else:
            # Créer une ligne avec Text + TextField pour afficher l'élément DICOM
            tag_text = ft.Text(value=f"{indent}{element.name} [{element.tag}]:", width=300)
            value_field = ft.TextField(value=str(element.value), multiline=True)  # Champ de texte pour modifier la valeur
            field_mapping[value_field] = (element, parent)  # Associer le TextField avec l'élément DICOM
            row = ft.Row([tag_text, value_field], vertical_alignment="center")  # Disposition des éléments
            controls.append(row)
        return controls
    
    def process_dicom_file(e: ft.FilePickerResultEvent, ):
        """
        Fonction pour traiter le fichier DICOM sélectionné
        Paramètres :
            e (ft.FilePickerResultEvent) : L'événement contenant le fichier sélectionné
        """
        nonlocal dicom_dataset
        file_path = e.files[0].path if e.files else None  # Récupérer le chemin du fichier sélectionné
        if not file_path:  # Si aucun fichier n'est sélectionné, quitter la fonction
            return
        try:
            # Lecture du fichier DICOM
            dicom_dataset = pydicom.dcmread(file_path)
            # Nettoyer le conteneur précédent
            scrollable_container.controls.clear()
            field_mapping.clear()

            # Ajouter les balises et sous-balises au conteneur
            for element in dicom_dataset:
                scrollable_container.controls.extend(display_element(element))

        except InvalidDicomError:
            show_error(page, "Le fichier sélectionné n'est pas un fichier DICOM valide.")
            scrollable_container.controls.clear()
        except Exception as ex:
            show_error(page, f"Une erreur est survenue : {ex}")
            scrollable_container.controls.clear()
        page.update()
    
    def save_dicom_file(e: ft.FilePickerResultEvent):
        """
        Fonction pour sauvegarder le fichier DICOM avec les valeurs modifiées
        Paramètres :
            e (ft.FilePickerResultEvent) : L'événement contenant le chemin où sauvegarder le fichier
        """
        file_path = e.path if e.path else None  # Récupérer le chemin de sauvegarde du fichier
        if not file_path:  # Si aucun chemin n'est sélectionné, quitter la fonction
            return
        try:
            # Mettre à jour le dataset DICOM avec les valeurs modifiées
            for textfield, (element, parent) in field_mapping.items():
                new_value = textfield.value.strip()  # Lire la valeur directement du TextField
                if parent:  # Si l'élément est une sous-balise
                    parent[element.tag].value = new_value
                else:       # Si l'élément est une balise principale
                    element.value = new_value

            # Sauvegarder le fichier DICOM
            dicom_dataset.save_as(file_path)
            show_error(page, "Fichier DICOM sauvegardé avec succès.") 
        except Exception as ex:
            show_error(page, f"Une erreur est survenue lors de la sauvegarde : {ex}")
        page.update()

    # Ajout du gestionnaire d'événements au file picker
    file_picker.on_result = process_dicom_file
    save_file_picker.on_result = save_dicom_file

    # Ajouter file_picker à la page via page.overlay
    page.overlay.extend([file_picker, save_file_picker])

    # Bouton pour ouvrir le FilePicker et choisir un fichier DICOM
    pick_file_button = ft.ElevatedButton(
        text="Choisir un fichier DICOM",
        on_click=lambda _: file_picker.pick_files(dialog_title="Sélectionner un fichier DICOM"),
    )

    # Bouton pour sauvegarder le fichier DICOM
    save_file_button = ft.ElevatedButton(
        text="Sauvegarder le fichier DICOM",
        on_click=lambda _: save_file_picker.save_file(dialog_title="Enregistrer le fichier DICOM"),
    )

    # Construction de l'interface utilisateur principale
    content = Container(
        ft.Column(
            controls=[
                error_message,  # Zone pour afficher les messages d'erreur
                ft.Container(scrollable_container),  # Conteneur pour afficher les TextFields
                ft.Divider(),  # Diviseur entre les sections
                pick_file_button,  # Bouton pour choisir le fichier
                save_file_button  # Bouton pour sauvegarder le fichier
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

    return content
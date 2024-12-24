import flet as ft

def create_file_explorer(page):
    """
    Crée un conteneur défilable pour afficher les données DICOM.

    Paramètres :
        page (ft.Page) : Page principale de l'application.

    Retour :
        ft.Column : Un conteneur de type colonne avec une fonctionnalité de défilement.
    """
    
    return_column = ft.Column(
            height=page.height,  # Hauteur du conteneur ajustée à la page
            width=page.width-250,
            scroll="always",  # Active le défilement pour afficher un contenu de grande taille
            alignment=ft.MainAxisAlignment.CENTER
        )

    # Fonction pour ajuster la taille du container lorsque la fenêtre est redimensionnée
    def on_resize(e):
        return_column.height = page.height  # Ajuste la hauteur en fonction de la hauteur de la fenêtre
        return_column.width = page.width  # Ajuste la largeur en fonction de la hauteur de la fenêtre
        page.update()  # Met à jour la page pour appliquer le changement

    # Attacher l'événement de redimensionnement à la page
    page.on_resize = on_resize
    
    return return_column


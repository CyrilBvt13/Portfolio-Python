import flet as ft

def create_file_name():
    """
    Crée un conteneur pour afficher le nom d'un fichier sélectionné, avec un bouton de fermeture.

    Retour :
        tuple : Contient trois éléments :
            - filename_container (ft.Row) : Une ligne contenant le bouton pour afficher le nom du fichier 
              et un bouton pour fermer ou masquer cet affichage.
            - filename_button (ft.TextButton) : Un bouton affichant le nom du fichier. Il est invisible par défaut.
            - close_icon (ft.IconButton) : Un bouton avec une icône "fermer", pour masquer ou réinitialiser le conteneur.
    """

    # Bouton pour afficher le nom du fichier sélectionné (initialement invisible)
    filename_button = ft.TextButton(
        text=ft.Text(
            '',  # Texte vide par défaut
            weight=ft.FontWeight.BOLD  # Texte en gras
        ),
        style=ft.ButtonStyle(
            # Coloration du texte (optionnel, peut être ajoutée si nécessaire)
            # color=ft.colors.BLACK,
            overlay_color={"hovered": None},  # Supprime l'effet de survol
        ),
        visible=False  # Le bouton est caché par défaut
    )

    # Bouton pour fermer ou masquer le conteneur (initialement invisible)
    close_icon = ft.IconButton(ft.icons.CLOSE, visible=False)

    # Conteneur principal sous forme de ligne contenant le bouton et l'icône
    filename_container = ft.Row(
        controls=[
            filename_button,  # Bouton pour afficher le nom du fichier
            close_icon,  # Bouton pour fermer le conteneur
        ],
    )

    # Retourne le conteneur, le bouton et l'icône
    return filename_container, filename_button, close_icon
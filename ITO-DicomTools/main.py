import flet as ft
from pydicom.errors import InvalidDicomError

from views.routing import Router


def main(page: ft.Page):
    """
    Initialise et configure la page de l'application Flet, 
    puis définit un système de routage pour la navigation.

    Paramètres :
        page (ft.Page) : Objet représentant la page principale de l'application.
    """
    
    # Configuration de base de la page
    page.title = "ITO - Dicom Tools"  # Titre de la fenêtre
    page.vertical_alignment = ft.MainAxisAlignment.CENTER  # Alignement vertical du contenu
    page.theme_mode = ft.ThemeMode.LIGHT  # Thème clair
    page.window_width = 1000  # Largeur fixe de la fenêtre
    page.window_height = 600  # Hauteur fixe de la fenêtre
    #page.window_resizable = False  # Désactivation du redimensionnement de la fenêtre
    page.scroll = "adaptive"

    # Initialisation du routeur pour gérer la navigation
    router = Router(page)

    # Liaison de la fonction de changement de route au routeur
    page.on_route_change = router.route_change

    # Ajout asynchrone du contenu principal à la page
    page.add(
        ft.Row(
            [
                router.body,  # Contenu dynamique géré par le routeur
            ],
            #alignment=ft.MainAxisAlignment.CENTER  # Alignement centré horizontalement
        )
    )

    # Navigation initiale vers la route '/app'
    page.go('/app')

    # Mise à jour asynchrone de la page
    page.update()

# Démarrage de l'application avec la fonction principale
ft.app(target=main)
    


    

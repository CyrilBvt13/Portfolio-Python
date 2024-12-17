import flet as ft
from views.view_app import AppView

class Router:
    """
    Classe Router pour gérer le routage dans une application Flet.
    Permet de naviguer entre différentes vues en fonction de l'URL actuelle.

    Attributs :
        page (ft.Page) : La page principale de l'application Flet.
        ft (module) : Le module Flet pour la création d'interfaces utilisateur.
        routes (dict) : Un dictionnaire associant les chemins d'URL à leurs vues correspondantes.
        body (ft.Container) : Conteneur principal où le contenu de la vue active est affiché.
    """

    def __init__(self, page):
        """
        Initialise le routeur avec une page Flet et configure les routes.

        Paramètres :
            page (ft.Page) : La page principale de l'application Flet.
        """
        self.page = page
        self.ft = ft
        # Dictionnaire des routes, associant chaque chemin à sa vue
        self.routes = {
            "/app": AppView(page)  # Vue associée à la route "/app"
        }
        # Conteneur initialisé avec le contenu de la route par défaut
        self.body = ft.Container(content=self.routes['/app'])

    async def route_change(self, route):
        """
        Gère le changement de route. Met à jour le contenu du conteneur en fonction de la nouvelle route.

        Paramètres :
            route (ft.RouteChangeEvent) : L'événement de changement de route contenant la nouvelle URL.
        """
        # Met à jour le contenu du conteneur en fonction de la route demandée
        self.body.content = self.routes[route.route]
        # Rafraîchit l'affichage du conteneur
        await self.body.update_async()
from threading import Thread

# Imports Flask
from flask import Flask, jsonify
from flask_restful import Api
#from resources.routes import auth_bp, groups_bp
from resources.routes import initialize_routes
from web.utils.show_back_error import register_error_handlers  # Importer la gestion des erreurs

#Imports Flet
import flet as ft
from web.templates.routing import Router

# Création de l'application Flask
app_flask = Flask(__name__)

# Enregistrement des blueprints
#app_flask.register_blueprint(auth_bp)
#app_flask.register_blueprint(groups_bp)
api_flask = Api(app_flask)
initialize_routes(api_flask)

# Enregistrement des gestionnaires d'erreurs
register_error_handlers(app_flask)

# Fonction pour démarrer le serveur Flask
def start_flask_server():
    """
    Démarre le serveur Flask.
    """
    try:
        app_flask.run(host="127.0.0.1", port=5000, debug=False)
    except Exception as e:
        print(f"Erreur dans le serveur Flask : {e}")

# Fonction pour l'application Flet
def start_flet_server(page: ft.Page):
    """
    Démarre l'application Flet.
    """
    page.title = "EAI"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.bgcolor = ft.Colors.WHITE
    
    page.padding = 0
    
    #page.scroll = "adaptive"

    # Initialisation du routeur pour gérer la navigation
    router = Router(page)

    # Liaison de la fonction de changement de route au routeur
    page.on_route_change = router.route_change

    # Ajout asynchrone du contenu principal à la page
    page.add(
        ft.Row(
            controls=[
                router.body,  # Contenu dynamique géré par le routeur
            ],
        )
    )

    # Navigation initiale vers la route '/app'
    page.go('/app')

    # Mise à jour asynchrone de la page
    page.update()

# Fonction principale
if __name__ == "__main__":
    # Démarrer le serveur Flask dans un thread séparé
    flask_thread = Thread(target=start_flask_server, daemon=True)
    flask_thread.start()

    # Démarrer l'application Flet
    try:
        ft.app(target=start_flet_server)
    except Exception as e:
        print(f"Erreur dans le serveur Flet : {e}")
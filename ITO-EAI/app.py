from threading import Thread
import time
import requests

# Imports Flask
from flask import Flask, jsonify
from flask_restful import Api
from resources.routes import initialize_routes
from web.utils.show_back_error import register_error_handlers  # Importer la gestion des erreurs

#Imports Flet
import flet as ft
from web.templates.routing import Router

from utils.hl7.hl7_flow import load_active_flows


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

def wait_for_flask():
    """Attend que le serveur Flask soit prêt avant d’appeler l’API."""
    url = "http://127.0.0.1:5000/groups"
    max_retries = 3
    for i in range(max_retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("✅ Serveur Flask est prêt !")
                return
            time.sleep(1)
        except:
            print(f"⏳ Attente du serveur Flask... (Tentative {i+1}/{max_retries})")
            time.sleep(1)
    print("❌ Le serveur Flask n'est pas accessible après plusieurs tentatives.")

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
    print("🔄 Démarrage du back...")
    flask_thread = Thread(target=start_flask_server, daemon=True)
    flask_thread.start()

    # Attendre que Flask soit prêt avant de charger les flux
    wait_for_flask()
    
    # Charger les flux actifs après que Flask ait bien démarré
    load_active_flows()

    # Démarrer l'application Flet
    try:
        print("🔄 Démarrage du front...")
        ft.app(target=start_flet_server)     

    except Exception as e:
        print(f"Erreur dans le serveur Flet : {e}")

    # flet run --web app.py
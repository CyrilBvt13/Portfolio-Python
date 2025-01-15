from flask import jsonify

def handle_flask_error(error):
    """
    Gère toutes les exceptions dans le serveur Flask et retourne une réponse JSON.
    """
    response = {
        "error": str(error),
        "message": "Une erreur interne est survenue dans le serveur Flask.",
    }
    return jsonify(response), 500

def register_error_handlers(app):
    """
    Enregistre les gestionnaires d'erreurs sur l'application Flask.
    
    Arguments:
        app (Flask): L'instance Flask où enregistrer les gestionnaires d'erreurs.
    """
    app.register_error_handler(Exception, handle_flask_error)
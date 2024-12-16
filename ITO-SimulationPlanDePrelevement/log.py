import os
import sys
from datetime import datetime
from config import readConf

# Fonction pour écrire dans les logs si verbose est activé
def log(message):
    """
    Fonction pour écrire les logs dans un fichier log_DateDuJour.log
    """
    
    # Récupération des paramètres de configuration
    verbose = readConf()[3]  # Act
    
    # Si log_mode est activé (1), rediriger la sortie standard vers un fichier log
    if verbose == 1:
        log_filename = f"log_{datetime.now().strftime('%Y-%m-%d')}.log"
        with open(log_filename, "a") as log_file:
            log_file.write(f"{datetime.now()} - {message}\n")
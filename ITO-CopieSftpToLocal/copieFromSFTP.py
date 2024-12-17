import os
import paramiko
from datetime import datetime

# Dictionnaire pour stocker les variables issues du fichier de configuration
variables = {}

# Valeurs par défaut des paramètres SFTP
SFTP_HOST = ''            # Adresse du serveur SFTP
SFTP_PORT = 0             # Port du serveur SFTP
SFTP_USERNAME = ''        # Nom d'utilisateur pour l'authentification
SFTP_PASSWORD = ''        # Mot de passe pour l'authentification
REMOTE_PATH = ''          # Chemin distant sur le serveur SFTP
LOCAL_PATH = ''           # Chemin local pour télécharger les fichiers
LOG_FILE = ''             # Chemin du fichier log
VERBOSE = False           # Flag pour activer ou non les logs

# Lecture du fichier de configuration pour charger les paramètres
with open('config.txt', 'r') as fichier:
    lignes = fichier.readlines()
    for ligne in lignes:
        # Ignorer les lignes vides ou les commentaires
        if ligne.strip() == '' or ligne.strip().startswith('[') or ligne.strip().startswith('#'):
            continue
        # Extraire le nom de la variable et sa valeur
        nom_variable, valeur = ligne.strip().split('=')
        variables[nom_variable.strip()] = valeur.strip()

# Assignation des valeurs issues du fichier de configuration
for nom_variable, valeur in variables.items():
    if nom_variable == 'host':
        SFTP_HOST = valeur
    elif nom_variable == 'port':
        SFTP_PORT = int(valeur)
    elif nom_variable == 'username':
        SFTP_USERNAME = valeur
    elif nom_variable == 'password':
        SFTP_PASSWORD = valeur
    elif nom_variable == 'remote_path':
        REMOTE_PATH = valeur
    elif nom_variable == 'local_path':
        LOCAL_PATH = valeur
    elif nom_variable == 'log_file':
        LOG_FILE = valeur
    elif nom_variable == 'verbose':
        VERBOSE = bool(valeur)
    else:
        # Afficher un avertissement pour les variables non reconnues
        print('Variable non reconnue:', nom_variable)

# Afficher les paramètres SFTP chargés
#print(SFTP_HOST, SFTP_PORT, SFTP_USERNAME, SFTP_PASSWORD, REMOTE_PATH, LOCAL_PATH)

# Fonction pour écrire un message dans les logs si VERBOSE est activé
def log(message):
    if VERBOSE:
        with open(LOG_FILE, "a") as log_file:
            log_file.write(f"{datetime.now()} - {message}\n")  # Ajout d'un timestamp au message loggé
        print(message)

# Fonction pour établir la connexion au serveur SFTP
def connect_sftp():
    try:
        # Créer un transport Paramiko pour se connecter au serveur SFTP
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USERNAME, password=SFTP_PASSWORD)
        sftp = paramiko.SFTPClient.from_transport(transport)
        log("Connexion SFTP établie.")
        return sftp
    except Exception as e:
        log(f"Erreur lors de la connexion au serveur SFTP : {e}")
        return None

# Fonction pour télécharger les fichiers depuis le serveur SFTP
def download_files(sftp):
    try:
        log("Liste des fichiers sur le serveur SFTP :")
        files = sftp.listdir(REMOTE_PATH)  # Récupérer la liste des fichiers dans le répertoire distant
        for file in files:
            log(f"- {file}")

        # Créer le dossier local s'il n'existe pas
        if not os.path.exists(LOCAL_PATH):
            os.makedirs(LOCAL_PATH)

        # Télécharger chaque fichier de REMOTE_PATH vers LOCAL_PATH
        for file in files:
            remote_file_path = os.path.join(REMOTE_PATH, file)
            local_file_path = os.path.join(LOCAL_PATH, file)

            log(f"Téléchargement du fichier {file}...")
            sftp.get(remote_file_path, local_file_path)
            log(f"Fichier {file} téléchargé avec succès.")

        return files  # Retourner la liste des fichiers téléchargés
    except Exception as e:
        log(f"Erreur lors du téléchargement des fichiers : {e}")
        return []

# Fonction pour supprimer les fichiers distants après téléchargement
def delete_files(sftp, files):
    try:
        for file in files:
            remote_file_path = os.path.join(REMOTE_PATH, file)
            log(f"Suppression du fichier distant {file}...")
            sftp.remove(remote_file_path)  # Suppression du fichier sur le serveur
            log(f"Fichier {file} supprimé avec succès.")
    except Exception as e:
        log(f"Erreur lors de la suppression des fichiers distants : {e}")

# Fonction pour fermer la connexion SFTP proprement
def close_sftp(sftp):
    if sftp:
        sftp.close()
        log("Connexion SFTP fermée.")

# Point d'entrée principal du script
if __name__ == "__main__":
    log("Début du processus SFTP.")

    # Établir la connexion au serveur SFTP
    sftp = connect_sftp()
    if sftp:
        # Télécharger les fichiers depuis le serveur SFTP
        downloaded_files = download_files(sftp)

        # Supprimer les fichiers distants si le téléchargement a réussi
        if downloaded_files:
            delete_files(sftp, downloaded_files)

        # Fermer la connexion SFTP
        close_sftp(sftp)

    log("Processus SFTP terminé.")
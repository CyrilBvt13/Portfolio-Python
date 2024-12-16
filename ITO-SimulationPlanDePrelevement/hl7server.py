import asyncio
from hl7.mllp import start_hl7_server
from hl7Receiver import messageReceiver

from log import log
from config import readConf

# Variable globale pour suivre l'état du serveur (démarré ou arrêté)
isStarted = False

# Fonction asynchrone pour récupérer l'état actuel du serveur
async def getIsStarted():
    """
    Retourne l'état actuel du serveur (True si démarré, False sinon).
    """
    return isStarted

# Fonction asynchrone pour définir l'état actuel du serveur
async def setIsStarted(value):
    """
    Définit l'état actuel du serveur.
    Paramètre :
        value (bool) : True pour indiquer que le serveur est démarré, False sinon.
    """
    global isStarted
    isStarted = value

# Fonction asynchrone pour démarrer le serveur HL7
async def startServer():
    """
    Démarre un serveur HL7 en utilisant le protocole MLLP (Minimal Lower Layer Protocol).
    Le serveur écoute sur un port défini dans le fichier de configuration.
    """
    input_port = int(readConf()[1])  # Lecture du port d'écoute depuis le fichier de configuration

    try:
        # Utilisation d'un gestionnaire de contexte pour démarrer et arrêter le serveur proprement
        isStarted = True
        async with await start_hl7_server(
            messageReceiver,  # Fonction appelée pour traiter les messages reçus
            port=input_port,  # Port d'écoute
            encoding='iso-8859/1'  # Encodage utilisé pour les messages HL7
        ) as hl7_server:
            # Maintenir le serveur en fonctionnement jusqu'à l'annulation
            await hl7_server.serve_forever()
    except asyncio.CancelledError:
        # Cette exception est levée lorsqu'une tâche asynchrone est annulée
        pass
    except Exception as e:
        # Gestion des autres exceptions
        log("Error occurred in main:", e)
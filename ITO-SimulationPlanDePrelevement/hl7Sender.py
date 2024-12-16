import asyncio

import hl7
from hl7.mllp import open_hl7_connection

from config import readConf
from log import log

async def messageSender(message):
    """
    Fonction pour envoyer un message HL7 à un destinataire via une connexion MLLP.

    Paramètres :
        message (str) : Le message HL7 à envoyer, sous forme de chaîne.

    Fonctionnement :
    1. Lit la configuration depuis le fichier `config.txt` pour obtenir l'adresse cible et le port.
    2. Établit une connexion HL7 avec le destinataire.
    3. Envoie le message HL7 spécifié.
    4. Attente et affichage de l'accusé de réception (ACK) du destinataire.
    5. Gère les délais et les erreurs potentielles pour garantir un fonctionnement robuste.

    Exceptions possibles :
        - asyncio.TimeoutError : Si la connexion ou l'attente d'une réponse dépasse le délai spécifié.
        - Erreurs liées au protocole HL7 ou à la connexion.
    """
    # Récupération des paramètres de configuration
    host = readConf()[0]  # Adresse cible (destination du message HL7)
    port = int(readConf()[2])  # Port d'émission pour envoyer le message HL7
    
    try:
        # Ouverture de la connexion HL7 vers le récepteur
        # Utilisation de `asyncio.wait_for` pour limiter le temps d'attente à 10 secondes
        hl7_reader, hl7_writer = await asyncio.wait_for(
            open_hl7_connection(host, port, encoding='iso-8859/1'),
            timeout=10,
        )

        # Parsing du message HL7 pour le convertir au format requis par la bibliothèque HL7
        hl7_message = hl7.parse(message, encoding='iso-8859/1')

        # Envoi du message HL7
        hl7_writer.writemessage(hl7_message)  # Écriture du message sur le canal
        await hl7_writer.drain()  # S'assurer que le message est réellement envoyé
        log(f'Message envoyé :\n {hl7_message}'.replace('\r', '\n'))

        # Attente de la réponse (ACK) du récepteur
        hl7_ack = await asyncio.wait_for(
            hl7_reader.readmessage(),  # Lecture du message de réponse
            timeout=10  # Limitation du temps d'attente pour l'ACK
        )
        log(f'ACK reçu :\n {hl7_ack}'.replace('\r', '\n'))

    except asyncio.TimeoutError:
        # Gestion d'une erreur de délai d'attente
        log(f"Erreur : la connexion ou l'attente de l'ACK a dépassé le délai de 10 secondes.")
    except Exception as e:
        # Gestion d'autres exceptions potentielles
        log(f"Une erreur s'est produite : {e}")

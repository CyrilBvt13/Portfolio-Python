import asyncio

from hl7transformer import transform_message
from hl7Sender import messageSender

from log import log

async def messageReceiver(hl7_reader, hl7_writer):
    """
    Fonction appelée chaque fois qu'une connexion socket est établie.
    Elle gère la réception, le traitement et l'envoi des messages HL7.

    Paramètres :
        hl7_reader : Objet permettant de lire les messages HL7 reçus.
        hl7_writer : Objet permettant d'écrire des messages HL7 à envoyer.

    Fonctionnement :
    1. Établit une connexion avec un client.
    2. Lit les messages HL7 entrants.
    3. Envoie un accusé de réception (ACK) pour chaque message reçu.
    4. Transforme le message HL7 reçu.
    5. Envoie le message transformé via le module `messageSender`.
    """
    peername = hl7_writer.get_extra_info("peername")
    log(f"Connection établie avec {peername}")
    log('')

    try:
        # Boucle pour écouter les messages entrants tant que la connexion est active
        while not hl7_writer.is_closing():
            # Lecture d'un message HL7
            hl7_message = await hl7_reader.readmessage()
            log(f'Message reçu :\n {hl7_message}'.replace('\r', '\n'))

            # Envoi d'un accusé de réception (ACK) au client
            hl7_writer.writemessage(hl7_message.create_ack())
            await hl7_writer.drain()  # Attendre que les données soient envoyées

    except asyncio.IncompleteReadError:
        # Gestion des erreurs de lecture. Si le writer n'est pas fermé, on le ferme proprement.
        if not hl7_writer.is_closing():
            hl7_writer.close()
            await hl7_writer.wait_closed()

    # Fermeture de la connexion
    log(f"Connexion fermée avec {peername}")
    log('')

    # Transformation du message HL7 reçu en un format spécifique
    transformed_message = transform_message(hl7_message)

    # Préparation du message transformé pour l'envoi
    send_message = ''
    for i in range(len(transformed_message)):
        # Ajout d'un caractère de fin de segment HL7 ('\r') après chaque segment
        trame = str(transformed_message[i]) + '\r'
        send_message += trame

    # Envoi du message transformé à un autre système via le module `messageSender`
    await messageSender(message=send_message)


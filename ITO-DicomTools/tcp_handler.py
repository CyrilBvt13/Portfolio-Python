import socket
import threading
import pydicom
from pynetdicom import AE, evt
from pydicom import dcmread
from pydicom.uid import UID, ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian
from pynetdicom.sop_class import (
    XRayRadiationDoseSRStorage,
    ModalityWorklistInformationFind
    # Ajouter d'autres SOP Class UID selon vos besoins
)
from views.view_error import show_error

def send_dicom_file(dicom_dataset, ip, port, aet, aec):
    """
    Envoie un fichier DICOM via TCP/IP, quel que soit son type.

    Paramètres :
        dicom_dataset (pydicom.dataset.FileDataset) : Dataset DICOM à envoyer.
        ip (str) : Adresse IP du destinataire.
        port (int) : Port du destinataire.
        aet (str) : AET (Application Entity Title) de l'émetteur.
        aec (str) : AEC (Application Entity Title) du destinataire.

    Retour :
        str : Message de succès ou d'erreur.
    """

    # Charger le fichier DICOM
    ds = dicom_dataset

    # Vérifier que le dataset contient un SOP Class UID valide
    if not hasattr(ds, "SOPClassUID"):
        return "Le fichier DICOM ne contient pas de SOP Class UID valide."

    sop_class_uid = UID(ds.SOPClassUID)

    # Créer une entité application (Application Entity - AE)
    ae = AE(ae_title=aet)

    # Ajouter les contextes pour les SOP Classes spécifiques
    supported_sop_classes = [
        XRayRadiationDoseSRStorage,
        ModalityWorklistInformationFind
        # Ajouter d'autres classes ici si nécessaire
    ]
    for sop_class in supported_sop_classes:
        ae.add_requested_context(sop_class)

    # Établir une association avec le serveur
    assoc = ae.associate(ip, port, ae_title=aec)

    if assoc.is_established:
        # Envoyer le fichier via le service C-STORE
        status = assoc.send_c_store(ds)

        # Vérifier le statut de la réponse
        if status:
            if status.Status == 0x0000:
                message = f"Fichier DICOM (SOPClassUID: {sop_class_uid}) envoyé avec succès!"
            else:
                message = f"Le serveur DICOM a rejeté l'envoi. Code de statut : {status.Status}"
        else:
            message = "Aucune réponse du serveur DICOM."

        # Libérer l'association
        assoc.release()
    else:
        message = f"Impossible d'établir une connexion avec le serveur DICOM (AET: {aec})."

    return message

def get_local_ip():
    """
    Récupère l'adresse IP locale du poste sur lequel tourne le programme.

    Retour :
        str : Adresse IP locale.
    """
    try:
        # Création d'une socket temporaire pour détecter l'IP locale
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Se connecter à une IP externe arbitraire pour obtenir l'IP locale
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception as e:
        print(f"Erreur lors de la récupération de l'IP locale : {e}")
        return "127.0.0.1"  # Retourne localhost en cas d'erreur

def receive_dicom_file(page, port, aet):
    """
    Démarre un serveur DICOM pour recevoir un fichier, le stocker en mémoire,
    puis arrêter le serveur après la réception.

    Paramètres :
        page : Page de l'application (interface utilisateur).
        port (int) : Port pour les connexions entrantes.
        aet (str) : AET (Application Entity Title) du serveur.

    Retour :
        pydicom.dataset.FileDataset : Le dataset DICOM reçu.
    """

    # Récupérer l'adresse IP locale
    ip = get_local_ip()

    # Variable pour stocker le dataset reçu
    dicom_dataset = None

    # Événement pour signaler la réception du fichier
    receive_event = threading.Event()

    # Gestionnaire pour l'événement C-STORE
    def handle_store(event):
        """Gestionnaire pour les fichiers reçus via C-STORE."""
        nonlocal dicom_dataset
        try:
            # Obtenir le dataset DICOM envoyé
            ds = event.dataset

            # Conserver les métadonnées d'origine
            ds.file_meta = event.file_meta

            # Vérifier et définir les propriétés d'encodage
            if 'TransferSyntaxUID' in ds.file_meta:
                transfer_syntax = ds.file_meta.TransferSyntaxUID
                if transfer_syntax == ExplicitVRLittleEndian:
                    ds.is_little_endian = True
                    ds.is_implicit_VR = False
                elif transfer_syntax == ImplicitVRLittleEndian:
                    ds.is_little_endian = True
                    ds.is_implicit_VR = True
                elif transfer_syntax == ExplicitVRBigEndian:
                    ds.is_little_endian = False
                    ds.is_implicit_VR = False
                else:
                    raise ValueError(f"Syntaxe de transfert non supportée : {transfer_syntax}")

            # Stocker le dataset en mémoire
            dicom_dataset = ds
            show_error(page, f"Fichier reçu avec succès!")
            print(f"Dataset reçu et stocké en mémoire. SOPInstanceUID: {ds.SOPInstanceUID}")

            # Signaler que le fichier a été reçu
            receive_event.set()

            # Retourner un statut "Succès" au client
            return 0x0000
        except Exception as e:
            print(f"Erreur lors du traitement du dataset : {e}")
            # Retourner un statut "Erreur"
            return 0xC000

    # Créer une Application Entity (AE) avec le titre spécifié
    ae = AE(ae_title=aet)

    # Ajouter les contextes pour les SOP Classes spécifiques
    supported_sop_classes = [
        XRayRadiationDoseSRStorage,
        ModalityWorklistInformationFind
        # Ajouter d'autres classes ici si nécessaire
    ]
    for sop_class in supported_sop_classes:
        ae.add_supported_context(sop_class)

    # Associer le gestionnaire C-STORE
    handlers = [(evt.EVT_C_STORE, handle_store)]

    # Lancer le serveur (non bloquant)
    print(f"Serveur DICOM en attente sur {ip}:{port} avec AET '{aet}'...")
    show_error(page, f"Serveur DICOM en attente sur {ip}:{port}")
    server = ae.start_server((ip, port), evt_handlers=handlers, block=False)

    # Attendre la réception du fichier (avec timeout de 60 secondes)
    if not receive_event.wait(timeout=60):
        print("Aucun fichier reçu dans le délai imparti.")
        show_error(page, "Aucun fichier reçu dans le délai imparti.")
        server.shutdown()
        return None

    # Arrêter proprement le serveur après réception
    print("Arrêt du serveur DICOM.")
    server.shutdown()
    print("Serveur arrêté avec succès.")

    # Retourner le dataset DICOM reçu
    return dicom_dataset
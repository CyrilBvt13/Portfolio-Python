import socket
import pydicom
from pynetdicom import AE, evt
from pynetdicom.sop_class import XRayRadiationDoseSRStorage
from views.view_error import show_error

def send_dicom_file(dicom_dataset, ip, port, aet, aec):
    """
    Envoie un fichier DICOM via TCP/IP.

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

    # Vérifier que le fichier est bien un objet Radiation Dose Structured Report
    if ds.SOPClassUID != XRayRadiationDoseSRStorage:
        return f"Le fichier n'est pas un objet DICOM valide pour IHE-REM (Radiation Dose Structured Report)."

    # Créer une entité application (Application Entity - AE)
    ae = AE(ae_title=aet)

    # Ajouter le contexte pour Radiation Dose Structured Report Storage
    ae.add_requested_context(XRayRadiationDoseSRStorage)

    # Établir une association avec le serveur
    assoc = ae.associate(ip,port, ae_title=aec)

    if assoc.is_established:
        # Envoyer le fichier via le service C-STORE
        status = assoc.send_c_store(ds)

        # Vérifier le statut de la réponse
        if status:
            if status.Status == 0x0000:
                return f"Fichier DICOM envoyé avec succès!"
            else:
                return f"Rejeté par le serveur DICOM."
        else:
            return f"Aucune réponse du serveur."

        # Libérer l'association
        assoc.release()
    else:
        return f"Impossible d'établir une connexion avec le serveur DICOM."

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
        port (int) : Port pour les connexions entrantes.
        aet (str) : AET (Application Entity Title) du serveur.

    Retour :
        pydicom.dataset.FileDataset : Le dataset DICOM reçu.
    """

    # Récupérer l'adresse IP locale
    ip = get_local_ip()

    # Variable pour stocker le dataset reçu
    dicom_dataset = None

    # Gestionnaire pour l'événement C-STORE
    def handle_store(event):
        """Gestionnaire pour les fichiers reçus via C-STORE."""
        nonlocal dicom_dataset
        try:
            # Obtenir le dataset DICOM envoyé
            ds = event.dataset

            # Conserver les métadonnées d'origine
            ds.file_meta = event.file_meta

            # Stocker le dataset en mémoire
            dicom_dataset = ds
            show_error(page, f"Fichier reçu avec succès!")
            print(f"Dataset reçu et stocké en mémoire. SOPInstanceUID: {ds.SOPInstanceUID}")

            # Arrêter le serveur après réception
            print("Arrêt du serveur DICOM après réception du fichier.")
            server.shutdown()
            print("Serveur arrêté avec succès.")

            # Retourner un statut "Succès" au client
            return 0x0000
        except Exception as e:
            print(f"Erreur lors du traitement du dataset : {e}")
            # Retourner un statut "Erreur"
            return 0xC000

    # Créer une Application Entity (AE) avec le titre spécifié
    ae = AE(ae_title=aet)

    # Ajouter tous les SOP Classes de stockage supportés
    #for element in sop_class:
    #    ae.add_supported_context(element)
    ae.add_supported_context(XRayRadiationDoseSRStorage)

    # Associer le gestionnaire C-STORE
    handlers = [(evt.EVT_C_STORE, handle_store)]

    # Lancer le serveur (bloquant)
    print(f"Serveur DICOM en attente sur {ip}:{port} avec AET '{aet}'...")
    show_error(page, f"Serveur DICOM en attente sur {ip}:{port}")
    while(dicom_dataset == None):
        server = ae.start_server((ip, port), evt_handlers=handlers, block=False)

    # Retourner le dataset DICOM reçu
    return dicom_dataset
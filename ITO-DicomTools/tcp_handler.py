import socket
import pydicom
from pynetdicom import AE
from pynetdicom.sop_class import XRayRadiationDoseSRStorage

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
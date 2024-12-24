import socket
import pydicom

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
    print('Sending file to',ip,port)
    try:
        # Convertir le dataset DICOM en données binaires
        dicom_bytes = bytearray()
        with pydicom.filebase.DicomBytesIO() as dicom_io:
            dicom_dataset.save_as(dicom_io, write_like_original=True)
            dicom_bytes = dicom_io.getvalue()

        # Créer le socket TCP/IP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, port))

            # Créer un message DICOM basique avec l'en-tête
            aet_encoded = aet.encode('utf-8').ljust(16, b' ')  # Aligné sur 16 octets
            aec_encoded = aec.encode('utf-8').ljust(16, b' ')  # Aligné sur 16 octets
            header = aet_encoded + aec_encoded

            # Envoyer l'en-tête suivi des données DICOM
            sock.sendall(header + dicom_bytes)

        return f"Fichier DICOM envoyé avec succès à {ip}:{port}."

    except Exception as e:
        return f"Erreur lors de l'envoi : {e}"
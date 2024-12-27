import unittest
from unittest.mock import MagicMock, patch
from tcp_handler import send_dicom_file
import pydicom
import socket

class TestTcpHandler(unittest.TestCase):

    def setUp(self):
        """
        Initialisation des objets nécessaires pour les tests.
        """
        self.mock_dicom_dataset = MagicMock()
        self.ip = "127.0.0.1"
        self.port = 104
        self.aet = "TEST_AET"
        self.aec = "TEST_AEC"

    @patch("socket.socket")
    @patch("pydicom.filebase.DicomBytesIO")
    def test_send_dicom_file_success(self, mock_dicom_bytes_io, mock_socket):
        """
        Test : Envoi réussi d'un fichier DICOM via TCP/IP.
        """
        # Configurer le mock pour le flux DICOM
        mock_dicom_io = MagicMock()
        mock_dicom_bytes_io.return_value.__enter__.return_value = mock_dicom_io
        mock_dicom_io.getvalue.return_value = b"DICOM_DATA"

        # Configurer le mock pour le socket
        mock_sock_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_sock_instance

        # Appeler la fonction avec les mocks
        result = send_dicom_file(self.mock_dicom_dataset, self.ip, self.port, self.aet, self.aec)

        # Vérifications
        self.mock_dicom_dataset.save_as.assert_called_once_with(mock_dicom_io, write_like_original=True)
        mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_sock_instance.connect.assert_called_once_with((self.ip, self.port))

        # Vérification de l'envoi des données (en-tête + contenu DICOM)
        expected_header = self.aet.encode('utf-8').ljust(16, b' ') + self.aec.encode('utf-8').ljust(16, b' ')
        mock_sock_instance.sendall.assert_called_once_with(expected_header + b"DICOM_DATA")

        # Vérification du résultat
        self.assertEqual(result, f"Fichier DICOM envoyé avec succès à {self.ip}:{self.port}.")

    @patch("socket.socket")
    def test_send_dicom_file_socket_error(self, mock_socket):
        """
        Test : Gestion des erreurs lors de la connexion au socket.
        """
        # Simuler une erreur de connexion
        mock_socket.return_value.__enter__.side_effect = socket.error("Connection failed")

        # Appeler la fonction
        result = send_dicom_file(self.mock_dicom_dataset, self.ip, self.port, self.aet, self.aec)

        # Vérification du résultat
        self.assertIn("Erreur lors de l'envoi", result)
        self.assertIn("Connection failed", result)

    @patch("pydicom.filebase.DicomBytesIO")
    def test_send_dicom_file_invalid_dataset(self, mock_dicom_bytes_io):
        """
        Test : Gestion des erreurs lors de la conversion du dataset DICOM en bytes.
        """
        # Simuler une erreur lors de la conversion DICOM
        mock_dicom_io = MagicMock()
        mock_dicom_bytes_io.return_value.__enter__.return_value = mock_dicom_io
        self.mock_dicom_dataset.save_as.side_effect = Exception("Invalid DICOM dataset")

        # Appeler la fonction
        result = send_dicom_file(self.mock_dicom_dataset, self.ip, self.port, self.aet, self.aec)

        # Vérification du résultat
        self.assertIn("Erreur lors de l'envoi", result)
        self.assertIn("Invalid DICOM dataset", result)

if __name__ == "__main__":
    unittest.main()

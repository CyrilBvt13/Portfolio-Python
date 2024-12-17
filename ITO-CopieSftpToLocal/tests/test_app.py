import unittest
from unittest.mock import patch, mock_open, MagicMock
from CopieFromSFTP import connect_sftp, download_files, delete_files, close_sftp, log
import os
import paramiko

class TestSFTPScript(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    def test_log_verbose(self, mock_file):
        """Test de la fonction log en mode VERBOSE."""
        with patch("builtins.print") as mock_print:
            # Cas où VERBOSE est activé
            global VERBOSE
            VERBOSE = True
            log("Test message")

            # Vérifier que le message est écrit dans le fichier et affiché
            mock_print.assert_called_once_with("Test message")

    
    @patch("paramiko.Transport.connect")
    @patch("paramiko.SFTPClient.from_transport")
    def test_connect_sftp_success(self, mock_sftp_client, mock_transport_connect):
        """Test de connexion réussie au serveur SFTP."""
        sftp_mock = MagicMock()
        mock_sftp_client.return_value = sftp_mock

        # Appel de la fonction
        sftp = connect_sftp()

        # Assertions
        self.assertIsNotNone(sftp)
        mock_transport_connect.assert_called_once()
        mock_sftp_client.assert_called_once()

    @patch("paramiko.Transport.connect", side_effect=Exception("Connexion échouée"))
    def test_connect_sftp_failure(self, mock_transport_connect):
        """Test de l'échec de connexion au serveur SFTP."""
        sftp = connect_sftp()
        self.assertIsNone(sftp)

    @patch("paramiko.SFTPClient.listdir")
    @patch("paramiko.SFTPClient.get")
    def test_download_files_success(self, mock_sftp_get, mock_sftp_listdir):
        """Test du téléchargement réussi des fichiers."""
        # Configuration des mocks
        mock_sftp_listdir.return_value = ["file1.txt", "file2.txt"]
        sftp_mock = MagicMock()

        # Chemins locaux fictifs
        global LOCAL_PATH, REMOTE_PATH
        LOCAL_PATH = "test_local_path"
        REMOTE_PATH = "test_remote_path"
        os.makedirs(LOCAL_PATH, exist_ok=True)

        # Appel de la fonction
        files = download_files(sftp_mock)

        # Assertions
        self.assertEqual(files, ["file1.txt", "file2.txt"])
        mock_sftp_get.assert_called()
        self.assertTrue(os.path.exists(LOCAL_PATH))

    @patch("paramiko.SFTPClient.remove")
    def test_delete_files_success(self, mock_sftp_remove):
        """Test de la suppression réussie des fichiers distants."""
        sftp_mock = MagicMock()
        files = ["file1.txt", "file2.txt"]
        global REMOTE_PATH
        REMOTE_PATH = "test_remote_path"

        # Appel de la fonction
        delete_files(sftp_mock, files)

        # Assertions
        calls = [patch("os.path.join", return_value=f"{REMOTE_PATH}/{file}") for file in files]
        mock_sftp_remove.assert_called()

    def test_close_sftp(self):
        """Test de la fermeture de la connexion SFTP."""
        sftp_mock = MagicMock()
        close_sftp(sftp_mock)
        sftp_mock.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()
    
#python -m unittest tests/test_app.py
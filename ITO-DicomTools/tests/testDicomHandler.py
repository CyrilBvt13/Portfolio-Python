# A lancer avec la commande : python -m unittest discover -s tests

import unittest
from unittest.mock import MagicMock, patch
import pydicom
from pydicom.errors import InvalidDicomError
from dicom_handler import process_dicom_file, update_dicom_dataset_from_ui, save_dicom_file

class TestDicomHandler(unittest.TestCase):

    def setUp(self):
        # Initialisation des mocks pour les tests
        self.mock_event = MagicMock()
        self.mock_scrollable_container = MagicMock()
        self.mock_filename_button = MagicMock()
        self.mock_page = MagicMock()
        self.mock_field_mapping = {}
        self.mock_dicom_dataset = MagicMock()

    @patch('pydicom.dcmread')
    def test_process_dicom_file_valid(self, mock_dcmread):
        """Test : Traitement d'un fichier DICOM valide."""
        # Configurer le mock pour simuler un fichier DICOM valide
        mock_dcmread.return_value = self.mock_dicom_dataset
        self.mock_event.files = [MagicMock(path='valid.dcm', name='valid.dcm')]

        # Appeler la fonction à tester
        dicom_dataset, file_name = process_dicom_file(
            self.mock_event,
            self.mock_dicom_dataset,
            self.mock_scrollable_container,
            self.mock_filename_button,
            self.mock_page,
            self.mock_field_mapping
        )

        # Vérifications
        self.assertEqual(dicom_dataset, self.mock_dicom_dataset)
        self.assertEqual(file_name, 'valid.dcm')
        mock_dcmread.assert_called_once_with('valid.dcm')
        self.mock_scrollable_container.update.assert_called()
        self.mock_filename_button.update.assert_called()

    @patch('pydicom.dcmread')
    def test_process_dicom_file_invalid(self, mock_dcmread):
        """Test : Gestion d'un fichier DICOM invalide."""
        # Configurer le mock pour simuler une erreur DICOM invalide
        mock_dcmread.side_effect = InvalidDicomError
        self.mock_event.files = [MagicMock(path='invalid.dcm', name='invalid.dcm')]

        # Patch de la fonction d'affichage d'erreurs
        with patch('views.view_error.show_error') as mock_show_error:
            dicom_dataset, file_name = process_dicom_file(
                self.mock_event,
                self.mock_dicom_dataset,
                self.mock_scrollable_container,
                self.mock_filename_button,
                self.mock_page,
                self.mock_field_mapping
            )

            # Vérifications
            self.assertIsNone(file_name)
            self.assertEqual(dicom_dataset, self.mock_dicom_dataset)
            mock_show_error.assert_called_with(self.mock_page, "Le fichier sélectionné n'est pas un fichier DICOM valide.")
            self.mock_scrollable_container.controls.clear.assert_called()
            self.mock_filename_button.visible = False

    def test_update_dicom_dataset_from_ui(self):
        """Test : Mise à jour du dataset DICOM à partir de l'interface utilisateur."""
        # Configurer un mock d'élément et un champ modifiable
        mock_element = MagicMock()
        mock_element.value = "Old Value"
        mock_textfield = MagicMock(value="New Value")
        self.mock_field_mapping = {mock_textfield: (mock_element, None)}

        # Appeler la fonction à tester
        updated_dataset = update_dicom_dataset_from_ui(self.mock_dicom_dataset, self.mock_field_mapping)

        # Vérifications
        self.assertEqual(mock_element.value, "New Value")
        self.assertEqual(updated_dataset, self.mock_dicom_dataset)

    @patch('pydicom.FileDataset.save_as')
    def test_save_dicom_file_success(self, mock_save_as):
        """Test : Sauvegarde réussie d'un fichier DICOM."""
        # Configurer le chemin de sauvegarde
        self.mock_event.path = 'output.dcm'

        # Patch de la fonction d'affichage d'erreurs
        with patch('views.view_error.show_error') as mock_show_error:
            save_dicom_file(
                self.mock_event,
                self.mock_dicom_dataset,
                self.mock_field_mapping,
                self.mock_page
            )

            # Vérifications
            mock_save_as.assert_called_once_with('output.dcm')
            mock_show_error.assert_called_with(self.mock_page, "Fichier DICOM sauvegardé avec succès.")

    @patch('pydicom.FileDataset.save_as')
    def test_save_dicom_file_error(self, mock_save_as):
        """Test : Gestion des erreurs lors de la sauvegarde d'un fichier DICOM."""
        # Configurer le chemin de sauvegarde et simuler une erreur
        self.mock_event.path = 'output.dcm'
        mock_save_as.side_effect = Exception("Save error")

        # Patch de la fonction d'affichage d'erreurs
        with patch('views.view_error.show_error') as mock_show_error:
            save_dicom_file(
                self.mock_event,
                self.mock_dicom_dataset,
                self.mock_field_mapping,
                self.mock_page
            )

            # Vérifications
            mock_show_error.assert_called_with(self.mock_page, "Une erreur est survenue lors de la sauvegarde : Save error")

if __name__ == '__main__':
    unittest.main()

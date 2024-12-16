import unittest
from hl7 import parse
from unittest.mock import AsyncMock, MagicMock, patch
import io
import sys
import os
import asyncio
from datetime import datetime

# Importation des fonctions et classes à tester
from config import readConf, writeConf
from hl7transformer import transform_message
from hl7Receiver import messageReceiver
from hl7Sender import messageSender

class TestApp(unittest.TestCase):

    # Test de la fonction readConf
    @patch('builtins.open', new_callable=MagicMock)
    def test_readConf(self, mock_open):
        # Simule le contenu du fichier config.txt
        mock_open.return_value.__enter__.return_value.readlines.return_value = [
            'target=127.0.0.1\n',
            'input_port=5994\n',
            'output_port=5995\n',
            'log_mode=1\n'
        ]

        # Appelle la fonction à tester
        target, input_port, output_port, log_mode = readConf()

        # Assertions
        self.assertEqual(target, '127.0.0.1')
        self.assertEqual(input_port, '5994')
        self.assertEqual(output_port, '5995')
        self.assertEqual(log_mode, 1)

    
    #Test de la fonction readConf avec des valeurs manquantes
    @patch('builtins.open', new_callable=MagicMock)
    def test_readConf_with_missing_values(self, mock_open):
        # Simule un fichier config.txt avec des valeurs manquantes
        mock_open.return_value.__enter__.return_value.readlines.return_value = [
            'target=192.168.1.1\n',
            '# input_port=5994\n',  # Commentaire
            'output_port=7000\n'
        ]

        # Appelle la fonction à tester
        target, input_port, output_port, log_mode = readConf()

        # Assertions sur les valeurs par défaut ou extraites
        self.assertEqual(target, '192.168.1.1')
        self.assertEqual(input_port, '1')  # Valeur par défaut
        self.assertEqual(output_port, '7000')
        self.assertEqual(log_mode, 0)  # Valeur par défaut

    #Test de la fonction writeConf
    @patch('builtins.open', new_callable=MagicMock)
    def test_writeConf(self, mock_open):
        # Simule le contenu initial du fichier config.txt
        initial_content = [
            'target=127.0.0.1\n',
            'input_port=5994\n',
            'output_port=5995\n',
            'log_mode=0\n'
        ]
        
        mock_open.return_value.__enter__.return_value.readlines.return_value = initial_content

        # Appelle la fonction à tester
        writeConf('192.168.1.1', 7000, 8000, 1)

        # Vérifie que le fichier a été mis à jour avec les nouvelles valeurs
        updated_content = [
            'target=192.168.1.1\n',
            'input_port=7000\n',
            'output_port=8000\n',
            'log_mode=1\n'
        ]

        # Vérifie que `writelines` a été appelé avec le contenu mis à jour
        mock_open.return_value.__enter__.return_value.writelines.assert_called_once_with(updated_content)
    
    '''
    # Test de la fonction messageSender   
    @patch('hl7.mllp.open_hl7_connection')
    @patch('hl7.parse')
    @patch('config.readConf', return_value=('127.0.0.1', '5994', '5995', '0'))
    def test_messageSender_success(self, mock_readConf, mock_hl7_parse, mock_open_hl7_connection):
        """
        Teste si `messageSender` envoie correctement un message HL7 et reçoit l'ACK.
        """
        # Configurer les mocks
        mock_hl7_message = MagicMock()
        mock_hl7_parse.return_value = mock_hl7_message

        mock_hl7_reader = AsyncMock()
        mock_hl7_writer = AsyncMock()
        mock_hl7_reader.readmessage.return_value = 'MSH|^~\\&|ACK'

        mock_open_hl7_connection.return_value = (mock_hl7_reader, mock_hl7_writer)
        
        # Appeler la fonction `messageSender`
        asyncio.run(messageSender('MSH|^~\\&|TEST'))

        # Vérifier que `open_hl7_connection` a été appelé
        mock_open_hl7_connection.assert_called_once_with(
            '127.0.0.1', 5995, encoding='iso-8859/1'
        )
    
        # Vérifier que la configuration a été lue
        mock_readConf.assert_called() #La fonction est appelée 2 fois

        # Vérifier que le message HL7 a été analysé
        mock_hl7_parse.assert_called_once_with('MSH|^~\\&|TEST', encoding='iso-8859/1')

        # Vérifier que le message HL7 a été envoyé
        mock_hl7_writer.writemessage.assert_called_once_with(mock_hl7_message)
        mock_hl7_writer.drain.assert_called_once()

        # Vérifier que l'ACK a été reçu
        mock_hl7_reader.readmessage.assert_called_once()
    
    #Test de la fonction messageSender avec timeout
    @patch('hl7.mllp.open_hl7_connection', side_effect=asyncio.TimeoutError)
    @patch('config.readConf', return_value=('127.0.0.1', '5994', '5995', 0))
    def test_messageSender_timeout(self, mock_log, mock_readConf, mock_open_hl7_connection):
        """
        Teste si `messageSender` gère correctement une erreur de délai d'attente.
        """
        asyncio.run(messageSender('MSH|^~\\&|TEST'))

        # Vérifier que la configuration a été lue
        mock_readConf.assert_called_once()

    #Test si la fonction messageSender gère correctement une exception
    @patch('hl7.mllp.open_hl7_connection', side_effect=Exception("Erreur de connexion"))
    @patch('config.readConf', return_value=('127.0.0.1', '5994', '5995', 0))
    def test_messageSender_exception(self, mock_log, mock_readConf, mock_open_hl7_connection):
        """
        Teste si `messageSender` gère correctement une exception.
        """
        asyncio.run(messageSender('MSH|^~\\&|TEST'))

        # Vérifier que la configuration a été lue
        mock_readConf.assert_called_once()
    '''
    '''
    # Test de la fonction messageReceiver
    @patch('transform_message', return_value=[
        'MSH|^~\\&|ACK',
        'MSA|AA|12345',
        'PID|1||123456||Doe^John',
        'ORC|NW|45678',
    ])
    async def test_messageReceiver(self, mock_transform_message):
        """
        Teste si `messageReceiver` reçoit correctement un message HL7, 
        transforme le message et appelle `messageSender`.
        """
        # Mocker les lecteurs et écrivains HL7
        mock_hl7_reader = AsyncMock()
        mock_hl7_writer = MagicMock()

        # Simuler un message HL7 reçu
        mock_hl7_reader.readmessage.return_value = MagicMock(create_ack=MagicMock(return_value='ACK'))

        # Appeler la fonction `messageReceiver`
        with patch('messageSender', new_callable=AsyncMock) as mock_messageSender:
            await messageReceiver(mock_hl7_reader, mock_hl7_writer)

            # Vérifier que le message a été lu
            mock_hl7_reader.readmessage.assert_called_once()

            # Vérifier que l'ACK a été envoyé
            mock_hl7_writer.writemessage.assert_called_once_with('ACK')
            mock_hl7_writer.drain.assert_called_once()

            # Vérifier que `transform_message` a été appelé
            mock_transform_message.assert_called_once()

            # Vérifier que `messageSender` a été appelé avec le message transformé
            mock_messageSender.assert_called_once_with(message='MSH|^~\\&|ACK\rMSA|AA|12345\rPID|1||123456||Doe^John\rORC|NW|45678\r')
    '''
      
    
    # Création d'un message de test
    def setUp(self):
        """
        Initialise un message HL7 factice pour les tests.
        """
        # Message HL7 factice
        self.raw_message = (
            "MSH|^~\\&|APP1|FAC1|APP2|FAC2|202412161230||OML^O21^OML_O21|MSGID1234|P|2.5^FRA^2.5||||AL|FRA|8859/1|FR||\r"
            "PID|1||12345^^^HOSP^MR||DOE^JOHN||19800101|M|||123 MAIN ST^^CITY^ST^12345||555-555-5555\r"
            "ORC|NW|ORDER1|PLACER1||SC||1|||202412161230\r"
            "TQ1|1||||202412161330|||R\r"
            "OBR|1|ORDER1|PLACER1|TEST^TEST_DESC^L||||202412161230||||||12345\r"
            "SPM|1|||Autre|||||||||||||20241213143800||||||||||||\r"
        )
        self.message = parse(self.raw_message)
    
    # Test de la fonction transform_message 
    def test_transform_message(self):
        """
        Teste que la fonction `transform_message` modifie correctement les segments HL7.
        """
        # Transformation du message
        modified_segments = transform_message(self.message)

        # Vérifications pour le segment MSH
        self.assertIn("MSH|^~\\&|APP2|FAC2|APP1|FAC1|202412161230||ORL^O22^ORL_O22", modified_segments[0])

        # Vérifications pour le segment MSA
        self.assertEqual(modified_segments[1], "MSA|AA|MSGID1234")

        # Vérifications pour le segment PID
        self.assertIn("PID|1||12345^^^HOSP^MR||DOE^JOHN||19800101|M|||123 MAIN ST^^CITY^ST^12345||555-555-5555", modified_segments[2])

        # Vérifications pour le segment ORC
        self.assertIn("ORC|NW|ORDER1|ORDER1||SC||1|||202412161230", modified_segments[3])

        # Vérifications pour le segment TQ1
        self.assertIn("TQ1|1||||202412161330|||R", modified_segments[4])

        # Vérifications pour le segment OBR
        self.assertIn("OBR|1|ORDER1|ORDER1|TEST^TEST_DESC^L||||202412161230||||||12345", modified_segments[5])

        # Vérifications pour le segment SPM
        self.assertIn("SPM|1|||HEPLI^Tube Héparinate de Lithium^L|||||||||||||20241213143800||||||||||^Tube 4ml vert avec gel (Héparinate Li)^L||", modified_segments[6])

    #Test de la fonction transform_message si le message est invalide
    def test_invalid_message(self):
        """
        Teste que la fonction lève une exception si le message n'est pas valide.
        """
        invalid_message = "INVALID HL7 MESSAGE"

        with self.assertRaises(Exception):
            transform_message(parse(invalid_message))

# Lancer les tests
if __name__ == '__main__':
    unittest.main()
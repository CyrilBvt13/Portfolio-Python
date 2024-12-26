
# ITO-DicomTools

ITO-DicomTools est une application Python conçue pour faciliter la manipulation et la transmission des fichiers DICOM via TCP/IP. Elle propose une interface conviviale permettant de charger, afficher et envoyer des fichiers DICOM, en faisant un outil précieux pour les professionnels de l'imagerie médicale et les développeurs travaillant avec les normes DICOM.

---

## Auteur
- **Auteur Principal** : Cyril Bouvart

---

## Fonctionnalités

- **Charger des fichiers DICOM** : Sélectionnez et chargez des fichiers DICOM depuis votre système local.  
- **Afficher les métadonnées DICOM** : Affichez les métadonnées détaillées des fichiers DICOM chargés.  
- **Envoyer des fichiers DICOM** : Transmettez des fichiers DICOM à un serveur spécifié via TCP/IP.  
- **Configurer les paramètres réseau** : Définissez l'IP de destination, le port, l'AET (Application Entity Title) et l'AEC (Application Entity Call) pour la transmission DICOM.  
- **Démarrer un serveur TCP** : Lancez un serveur TCP pour écouter les fichiers DICOM entrants.  

---

## Utilisation

1. **Lancez l'application** :  

   ```bash
   python main.py
   ```

2. **Charger un fichier DICOM** :  

   - Cliquez sur le bouton "Ouvrir" pour ouvrir le sélecteur de fichiers.  
   - Sélectionnez le fichier DICOM souhaité sur votre système.  

3. **Afficher les métadonnées DICOM** :  

   - Une fois le fichier chargé, ses métadonnées sont affichées dans le conteneur déroulant.  

4. **Envoyer un fichier DICOM** :  

   - Renseignez l’IP de destination, le port, l’AET et l’AEC dans les champs correspondants.  
   - Cliquez sur le bouton "Envoyer" pour transmettre le fichier DICOM.  

5. **Démarrer un serveur TCP** :  

   - Entrez l’hôte et le port pour le serveur.  
   - Cliquez sur le bouton "Écoute TCP/IP" pour commencer à écouter les fichiers DICOM entrants.  

## Structure du code

L’application est structurée en plusieurs modules :  

- **main.py** : Point d’entrée de l’application. Configure l’interface utilisateur et gère les interactions.  

- **dicom_utils.py** : Contient des fonctions utilitaires pour charger et analyser les fichiers DICOM.  

  ```python
  import pydicom

  def load_dicom_file(file_path):
      """
      Charge un fichier DICOM à partir du chemin spécifié.

      Paramètres :
          file_path (str) : Le chemin du fichier DICOM.

      Retour :
          pydicom.dataset.FileDataset : Le dataset DICOM chargé.
      """
      return pydicom.dcmread(file_path)
  ```

- **network_utils.py** : Fournit des fonctions pour envoyer des fichiers DICOM via TCP/IP et démarrer un serveur TCP.  

  ```python
  import socket

  def send_dicom_file(dicom_dataset, ip, port, aet, aec):
      """
      Envoie un fichier DICOM via TCP/IP à la destination spécifiée.

      Paramètres :
          dicom_dataset (pydicom.dataset.FileDataset) : Le dataset DICOM à envoyer.
          ip (str) : L'adresse IP de destination.
          port (int) : Le port de destination.
          aet (str) : Application Entity Title de l’émetteur.
          aec (str) : Application Entity Title du récepteur.
      """
      # Détails de l'implémentation...
  ```

  ```python
  import socket

  def start_tcp_server(host, port):
      """
      Démarre un serveur TCP pour écouter les fichiers DICOM entrants.

      Paramètres :
          host (str) : L'adresse IP de l’hôte à lier au serveur.
          port (int) : Le port à lier au serveur.
      """
      # Détails de l'implémentation...
  ```

---

## Dépendances

- [pydicom](https://pydicom.github.io/) : Pour lire et écrire des fichiers DICOM.  
- [flet](https://flet.dev/) : Pour construire l’interface utilisateur.  

---

## Exécutable
Un executable "stand-alone" permet de lancer le programme sans nécessité d'installer Python sur le serveur local.

Pour recompiler l'executable : 
```bash
 flet build windows
 ```

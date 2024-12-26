
# ITO-DicomTools

ITO-DicomTools est une application Python conçue pour manipuler des fichiers DICOM. Elle permet notamment d'ouvrir, modifier, sauvegarder et transmettre un fichier DICOM en TCP/IP.

---

## Auteur
- **Auteur Principal** : Cyril Bouvart

---

## Fonctionnalités

- **Charger des fichiers DICOM** : Sélectionnez et chargez des fichiers DICOM depuis votre système local.  
- **Afficher les métadonnées DICOM** : Affichez les métadonnées détaillées des fichiers DICOM chargés.
- **Sauvegarder les métadonnées DICOM** : Sauvegarder les fichiers DICOM modifiés.
- **Envoyer des fichiers DICOM** : Transmettez des fichiers DICOM à un serveur spécifié via TCP/IP.  

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
   -  
3. **Sauvegarder un fichier DICOM** :  

   - Une fois le fichier modifié, cliquez sur le bouton "Sauvegarder" pour enregistrer vos modifications.

5. **Envoyer un fichier DICOM** :  

   - Renseignez l’IP de destination, le port, l’AET et l’AEC dans les champs correspondants.  
   - Cliquez sur le bouton "Envoyer" pour transmettre le fichier DICOM.  

## Structure du code

L’application est structurée en plusieurs modules :  

- **main.py** : Point d’entrée de l’application. Configure l’interface utilisateur et gère les interactions.  

- **dicom_handler.py** : Contient des fonctions utilitaires pour charger et analyser les fichiers DICOM.  

- **tcp_handler.py** : Contient des fonctions utilitaires pour envoyer les fichiers DICOM par TCP/IP.
- 
- **views** : vues correspondantes à l'interface graphique.

## Dépendances

- [pydicom](https://pydicom.github.io/) : Pour lire et écrire des fichiers DICOM.  
- [flet](https://flet.dev/) : Pour construire l’interface utilisateur.  

---

## Exécutable
Une version "stand alone" permet d'utiliser l'application sur un serveur sans nécessité d'installer Python et ses dépendances.

Pour recompiler l'executable : 
```bash
 flet build windows
 ```

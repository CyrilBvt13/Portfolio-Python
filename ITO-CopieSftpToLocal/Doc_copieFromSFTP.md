# Documentation Technique du Script SFTP

## Description
Ce projet est un script Python permettant d'automatiser la copie de fichiers d'un **SFTP** distant vers un répertoire local. Le script se connecte au serveur distant, télécharge les fichiers d'un répertoire spécifique, les enregistre localement, puis supprime les fichiers distants après téléchargement.

Le projet est conçu pour être configurable via un fichier `config.txt`.

**Il est uniquement utilisable à des fins de tests et non pas en production**

---

## Fonctionnalités Principales
1. **Connexion sécurisée à un serveur SFTP** via la bibliothèque `paramiko`.
2. **Téléchargement automatique** des fichiers d'un répertoire distant vers un répertoire local.
3. **Suppression des fichiers distants** après téléchargement.
4. **Journalisation des opérations** dans un fichier de log lorsque le mode verbose est activé.

---

## Prérequis
### Logiciels et Bibliothèques
- Python 3.x
- Bibliothèque `paramiko` pour la gestion des connexions SFTP.

Pour installer la bibliothèque `paramiko`, utilisez :
```bash
pip install paramiko
```

### Fichier de Configuration : `config.txt`
Le fichier `config.txt` contient les paramètres nécessaires au fonctionnement du script. Voici un exemple :

```plaintext
host=example.com
port=22
username=my_user
password=my_password
remote_path=/chemin/distant
local_path=./chemin/local
log_file=./logs/sftp.log
verbose=True
```

#### Description des paramètres :
| **Paramètre**    | **Description**                         |
|------------------|-----------------------------------------|
| `host`          | Adresse du serveur SFTP.                |
| `port`          | Port de connexion SFTP (par défaut 22). |
| `username`      | Nom d'utilisateur pour l'accès SFTP.    |
| `password`      | Mot de passe pour l'accès SFTP.         |
| `remote_path`   | Chemin distant sur le serveur SFTP.     |
| `local_path`    | Chemin local pour stocker les fichiers. |
| `log_file`      | Chemin vers le fichier de logs.         |
| `verbose`       | Active ou désactive les logs (True/False). |

---

## Architecture du Code
### Fichiers
- `copieFromSFTP.py` : Script principal contenant les fonctions pour se connecter, télécharger et supprimer les fichiers.
- `test_sftp_script.py` : Tests unitaires pour valider le fonctionnement du script.

### Fonctions Principales
| **Fonction**         | **Description**                                                                 |
|-----------------------|-------------------------------------------------------------------------------|
| `connect_sftp()`      | Établit une connexion SFTP sécurisée et retourne l'objet `SFTPClient`.        |
| `download_files()`    | Télécharge les fichiers du répertoire distant vers le répertoire local.       |
| `delete_files()`      | Supprime les fichiers du répertoire distant après téléchargement.             |
| `close_sftp()`        | Ferme proprement la connexion SFTP.                                           |
| `log()`               | Enregistre les messages dans un fichier de log si le mode verbose est activé. |

### Schéma d'Exécution
1. Chargement de la configuration depuis `config.txt`.
2. Connexion au serveur SFTP.
3. Téléchargement des fichiers depuis le répertoire distant vers le répertoire local.
4. Suppression des fichiers distants après téléchargement.
5. Journalisation des opérations dans le fichier log.
6. Fermeture de la connexion.

---

## Exécution du Script
1. Placez le fichier `config.txt` dans le même répertoire que le script `copieFromSFTP.py`.
2. Exécutez le script principal :
   ```bash
   python sftp_script.py
   ```
3. Vérifiez les fichiers téléchargés dans le dossier local configuré.
4. Consultez les logs dans le fichier défini dans `config.txt` si `verbose=True`.

---

## Tests Unitaires
Le fichier `test_sftp_script.py` contient des tests pour valider les fonctionnalités principales.

### Exécution des Tests
Exécutez les tests unitaires avec la commande suivante :
```bash
python -m unittest test_sftp_script.py
```

Les fonctionnalités testées incluent :
- Connexion SFTP réussie ou échouée.
- Téléchargement des fichiers.
- Suppression des fichiers distants.
- Fermeture de la connexion.
- Journalisation des messages.

---

## Exécutable
Un executable "stand-alone" permet de lancer le programme sans nécessité d'installer Python sur le serveur local. Le fichier `config.txt` doit se trouver dans le même répertoire que l'éxecutable pour que celui-ci fonctionne.

Pour recompiler l'executable : 
```bash
 pyinstaller --onefile --noconsole .\copieFromSFTP.py
 ```
---

## Auteurs
- **Auteur Principal** : Cyril Bouvart
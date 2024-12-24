
# Documentation Technique de l'Application ITO - Dicom Tools

## Introduction
ITO - Dicom Tools est une application développée en Python avec le framework **Flet**. 
Elle permet de charger, afficher, modifier et sauvegarder des fichiers DICOM. 
Le projet est structuré en modules pour une meilleure lisibilité et maintenabilité du code.

---

## Auteur
- **Auteur Principal** : Cyril Bouvart

---

## Fonctionnalités Principales
1. **Chargement de fichiers DICOM** : 
   - Sélection et affichage des balises et données contenues dans un fichier DICOM.
2. **Modification des données DICOM** :
   - Edition directe des valeurs des balises.
3. **Sauvegarde des fichiers DICOM** :
   - Enregistrement des modifications apportées dans un nouveau fichier.

---

## Structure du Projet
### Fichiers Principaux

- `main.py` : Point d'entrée de l'application.
- `views/routing.py` : Gestionnaire de routage des différentes vues.
- `views/view_app.py` : Vue principale de l'application.
- `views/dicom_handler.py` : Gestion des fichiers DICOM (chargement, affichage, modification, sauvegarde).
- `views/ui_components.py` : Composants UI réutilisables.

### Détails des Modules
#### `main.py`
Configure la page principale de l'application et initialise le routeur pour naviguer entre les vues.

#### `routing.py`
Gère les routes de l'application. Par exemple :
- `/app` : Vue principale.

#### `view_app.py`
Crée l'interface utilisateur principale, composée :
- d'un menu latéral pour les actions utilisateur,
- d'un conteneur défilable pour afficher les données DICOM.

#### `dicom_handler.py`
- **`process_dicom_file`** : Charge un fichier DICOM et affiche ses données.
- **`save_dicom_file`** : Sauvegarde les modifications apportées à un fichier DICOM.

#### `ui_components.py`
- **`create_menu`** : Génère le menu latéral avec les boutons d'action.
- **`create_scrollable_container`** : Crée un conteneur défilable pour afficher les données DICOM.

---

## Exemple de Fonctionnalités
### Chargement d'un Fichier DICOM

Le fichier est chargé via un `FilePicker`. La fonction **`process_dicom_file`** extrait les balises du fichier et les affiche dans un conteneur défilable.

```python
def process_dicom_file(event, dicom_dataset, scrollable_container, page, field_mapping):
    # Traitement du fichier DICOM
    ...
```

### Sauvegarde des Modifications

Les modifications sont enregistrées grâce à la fonction **`save_dicom_file`**. Elle récupère les données modifiées depuis l'interface et met à jour le fichier DICOM.

```python
def save_dicom_file(event, dicom_dataset, field_mapping, page):
    # Sauvegarde des modifications
    ...
```

---

## Interface Utilisateur
### Menu Latéral
Contient deux boutons :
1. **Choisir un fichier DICOM** : Ouvre un sélecteur de fichiers pour charger un fichier DICOM.
2. **Sauvegarder le fichier DICOM** : Sauvegarde les modifications apportées.

### Conteneur Défilable
Affiche dynamiquement les balises et sous-balises du fichier DICOM avec des champs modifiables.

---

## Dépendances
- **Python** : Version 3.8 ou supérieure.
- **Bibliothèques** :
  - `flet`
  - `pydicom`

Installation des dépendances :
```bash
pip install flet pydicom
```

---

## Lancement de l'Application
Exécutez le fichier principal `main.py` :
```bash
python main.py
```

---

## Exécutable
Un executable "stand-alone" permet de lancer le programme sans nécessité d'installer Python sur le serveur local.

Pour recompiler l'executable : 
```bash
 pyinstaller --onefile --noconsole .\main.py
 ```

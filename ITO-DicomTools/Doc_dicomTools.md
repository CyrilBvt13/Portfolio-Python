# Documentation Technique de l'Application DICOM Viewer

## Introduction

Cette application permet de visualiser, modifier et sauvegarder des fichiers DICOM. Elle offre une interface utilisateur permettant de charger un fichier DICOM, de modifier ses valeurs, et de sauvegarder le fichier modifié. L'application utilise Flet pour l'interface utilisateur et PyDICOM pour le traitement des fichiers DICOM.

**Ce programme doit être utilisé exclusivement sur votre poste et non sur un serveur.**

---

## Fonctionnalités

- **Chargement de fichiers DICOM** : Permet à l'utilisateur de sélectionner un fichier DICOM via un explorateur de fichiers.
- **Affichage des balises DICOM** : Les balises et leurs valeurs sont affichées dans un format modifiable à l'aide de champs de texte.
- **Modification des balises** : Les utilisateurs peuvent modifier les valeurs des balises DICOM via des champs de texte.
- **Sauvegarde du fichier DICOM** : Après modification, l'utilisateur peut sauvegarder les changements dans un nouveau fichier DICOM.

---

## Structure du Projet

Le projet est organisé en plusieurs fichiers :

- `app_view.py` : Contient la logique de l'interface utilisateur (UI) et la gestion des événements liés à l'affichage et à la modification des fichiers DICOM.
- `view_error.py` : Contient la fonction `show_error` pour afficher des messages d'erreur.
- `main.py` : Point d'entrée de l'application où l'interface est lancée.

---

## Détails des Composants

### `app_view.py`

Ce fichier contient la logique principale pour la gestion de l'interface utilisateur. Il inclut la sélection et le traitement des fichiers DICOM, ainsi que l'affichage des balises DICOM.

#### Fonction `AppView(page)`

Cette fonction crée et gère l'interface utilisateur pour l'application.

**Paramètres** :
- `page` (ft.Page) : L'objet représentant la page de l'application.

**Retour** :
- Un conteneur `content` qui contient tous les éléments de l'interface utilisateur.

#### Fonction `display_element(element, level=0, parent=None)`

Affiche une balise DICOM et ses sous-balises. Cette fonction est récursive et permet de gérer les séquences (balises avec sous-balises).

**Paramètres** :
- `element` (pydicom.dataset.Dataset) : L'élément DICOM à afficher.
- `level` (int) : Le niveau d'indentation pour l'affichage (utilisé pour les sous-balises).
- `parent` (object) : L'élément parent, si applicable.

**Retour** :
- Une liste de contrôles Flet (`ft.Row`, `ft.Text`, `ft.TextField`) pour afficher les balises et leurs valeurs.

#### Fonction `process_dicom_file(e)`

Traite le fichier DICOM sélectionné par l'utilisateur et l'affiche dans l'interface.

**Paramètres** :
- `e` (ft.FilePickerResultEvent) : L'événement déclenché lors de la sélection d'un fichier.

#### Fonction `save_dicom_file(e)`

Sauvegarde le fichier DICOM avec les valeurs modifiées par l'utilisateur.

**Paramètres** :
- `e` (ft.FilePickerResultEvent) : L'événement déclenché lors de la demande de sauvegarde.

### `view_error.py`

Ce fichier contient la fonction `show_error`, qui affiche un message d'erreur dans une boîte de dialogue.

#### Fonction `show_error(page, message)`

Affiche une boîte de dialogue avec le message d'erreur spécifié.

**Paramètres** :
- `page` (ft.Page) : L'objet représentant la page de l'application.
- `message` (str) : Le message d'erreur à afficher.

## Fonctionnement de l'Application

### Sélectionner un fichier DICOM

L'utilisateur peut sélectionner un fichier DICOM en cliquant sur le bouton **Choisir un fichier DICOM**. Cela ouvre un sélecteur de fichiers permettant de choisir un fichier. Une fois le fichier sélectionné, l'application l'affiche dans l'interface.

### Modification des Balises DICOM

Les balises DICOM sont affichées sous forme de champs de texte. L'utilisateur peut modifier ces champs et les modifications sont mises à jour en temps réel dans le dataset DICOM.

### Sauvegarde du fichier DICOM

Après avoir effectué des modifications, l'utilisateur peut sauvegarder le fichier en cliquant sur le bouton **Sauvegarder le fichier DICOM**. Un sélecteur de fichiers s'ouvre, permettant à l'utilisateur de choisir l'emplacement et le nom du fichier.

### Gestion des Erreurs

En cas d'erreur (par exemple, si le fichier sélectionné n'est pas un fichier DICOM valide), un message d'erreur est affiché à l'utilisateur via une boîte de dialogue.

---

## Dépendances

L'application utilise les bibliothèques suivantes :

- **Flet** : Pour la création de l'interface utilisateur.
- **pydicom** : Pour la lecture et l'écriture des fichiers DICOM.

### Installation

1. Clonez le dépôt :
    ```bash
    git clone <url-du-dépôt>
    ```
2. Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

### Exécution

Pour lancer l'application, exécutez le fichier `main.py` :

```bash
python main.py
```

---

## Exécutable
Un executable "stand-alone" permet de lancer le programme sans nécessité d'installer Python sur le poste local. 

Pour recompiler l'executable : 
```bash
 pyinstaller --onefile --noconsole .\main.py
 ```
---

## Auteurs
- **Auteur Principal** : Cyril Bouvart
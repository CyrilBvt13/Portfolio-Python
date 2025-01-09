
# **Dicom Tools V0.1.1**

### **Description**
Cette application permet :
- l'ouverture et la sauvegarde de fichier DICOM (.dcm)
- la réception et la transmission de fichiers DICOM via TCP/IP
- l'édition des fichiers ouverts et reçus

---

## **Table des Matières**

1. [Contribution](#contribution)
2. [Installation](#installation)  
3. [Configuration](#configuration)  
   - [Pré-requis](#pré-requis)
4. [Utilisation](#utilisation)  
   - [Ouverture de fichiers DICOM](#ouverture-de-fichiers-dicom)  
   - [Réception de fichiers DICOM](#réception-de-fichiers-dicom)  
   - [Édition des métadonnées](#édition-des-métadonnées)  
   - [Sauvegarde de fichiers DICOM](#sauvegarde-de-fichiers-dicom)  
   - [Transmission de fichiers DICOM](#transmission-de-fichiers-dicom)  
5. [FAQ et dépannage](#faq-et-dépannage)  


---

## **Contribution**

Auteur principal : Cyril Bouvart

---

## **Installation**

Dezippez l'archive DicomTools.zip. Celle ci contient un executable dicomtools.exe permettant de lancer l'application.

---

## **Configuration**

### **Pré-requis**

Aucun prérequis nécessaires : l'application tourne en standalone.

---

## **Utilisation**

### **Ouverture de fichiers DICOM**
1. Pour ouvrir un fichier DICOM depuis votre poste, cliquez sur **Ouvrir** pour faire apparaitre la pop-up de sélection de fichier.
2. Une fois le fichier ouvert, il est affiché dans l'interface utilisateur. A tout moment vous pourrez revenir dessus en cliquant sur **le nom du fichier** en haut de la fenêtre.
3. Pour fermer le fichier ouvert, cliquez sur la **croix** en haut à droite de l'interface utilisateur.

### **Réception de fichiers DICOM**
1. Ouvrez l'onglet de réception.  
2. Configurez les champs suivants :  
   - **Port**  
   - **AET Émetteur**  
3. Cliquez sur **Recevoir** pour lancer le serveur DICOM.  
4. Une fois le fichier reçu, il est affiché dans l'interface utilisateur.  

### **Édition des métadonnées**
1. Après ouverture/réception, utilisez l'interface pour visualiser les tags DICOM.  
2. Modifiez les champs nécessaires dans les zones de texte associées.  

### **Sauvegarde de fichiers DICOM**
1. Pour enregistrer sur votre poste le fichier DICOM ouvert, cliquez sur **Sauvegarder** pour faire apparaitre la pop-up d'enregistrement.

### **Transmission de fichiers DICOM**
1. Pour transmettre via TCP/IP le fichier ouvert, configurez les informations suivantes dans l'onglet **Émission** :  
   - **Adresse IP**  
   - **Port**  
   - **AET Récepteur**  
2. Cliquez sur **Envoyer** pour transmettre le fichier au destinataire.  

---

## **FAQ et dépannage**

### **Problèmes fréquents**
1. **Erreur de transfert syntax UID :**
   - L'application ne prend en charge que les Sop Class XRayRadiationDoseSRStorage et ModalityWorklistInformationFind. Si besoin de rajouter un autre type de fichier, merci de contacter l'auteur.
3. **Échec de l'association DICOM :**
   - Vérifiez l'AET, le port et l'IP du destinataire.





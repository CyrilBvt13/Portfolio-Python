# EAI Médical

## 1. Fonctionnalités principales
- Réception, modification et émission de fichiers :
	- Formats supportés : HL7, HPRIM XML, CSV.
	- Modifications effectuées selon des règles personnalisables.
- Modes de transmission :
	- Réception et émission via TCP/IP.
	- Réception et émission via SFTP.
- Interface utilisateur :
	- Application web avec interface graphique développée en Flet.
	- Authentification utilisateur.
- Fonctionnement :
	- Fonctionne comme un service sur un serveur Windows.

---

## 2. Architecture et arborescence des fichiers

Scenario type :
- L'application reçoit un message par SFTP ou TCP/IP
- L'application applique des modifications enregistrées par l'utilisateur au format json
- L'application renvoie le message modifié par SFTP ou TCP/IP

L'interface permet à l'utilisateur :
- De créer des flux (réception, modification, émission)
- D'appliquer des modifications pour chaque flux
- De visualiser les messages reçus et transmis après modification

Sera stocké en base json :
- Les utilisateurs
- Le paramétrage des flux
- Les modificateurs

```
EAI_Medical/
├── app.py               # Point d'entrée principal de l'application.
├── config/
│   ├── settings.py      # Configuration des paramètres (TCP/IP, SFTP, etc.).
│   └── logging.conf     # Configuration des logs.
│ 
├── core/
│   ├── hl7_processor.py # Gestion et traitement des fichiers HL7.
│   ├── hprim_processor.py # Gestion et traitement des fichiers HPRIM XML.
│   ├── csv_processor.py # Gestion et traitement des fichiers CSV.
│   ├── file_manager.py  # Gestion des fichiers reçus/envoyés.
│   ├── transmission.py  # Gestion des transmissions TCP/IP et SFTP.
│   └── rule_engine.py # Gestion des règles de modifications des fichiers.
│ 
├── services/
│   ├── service_manager.py # Gestion du service Windows.
│  
├── user_auth/
│   ├── auth.py          # Gestion de l'authentification des utilisateurs.
│   ├── models.py        # Modèles pour les utilisateurs (base de données).
│   └── routes.py        # Routes liées à l'authentification (login, logout).
│ 
├── web/
│   ├── interface.py     # Interface graphique en Flet.
│   └── templates/       # Templates pour l'affichage web.
│ 
├── utils/
│   ├── hl7_parser.py    # Fonctions utilitaires pour traiter les fichiers HL7.
│   ├── xml_utils.py     # Fonctions utilitaires pour traiter XML (HPRIM).
│   ├── csv_utils.py     # Fonctions utilitaires pour le CSV.
│   ├── tcp_utils.py     # Fonctions utilitaires pour TCP/IP.
│   └── sftp_utils.py    # Fonctions utilitaires pour SFTP.
│ 
├── tests/
│   ├── test_hl7.py      # Tests pour les fichiers HL7.
│   ├── test_hprim.py    # Tests pour les fichiers HPRIM XML.
│   ├── test_csv.py      # Tests pour les fichiers CSV.
│   ├── test_auth.py     # Tests pour l'authentification.
│   └── test_service.py  # Tests pour les services (TCP/IP, SFTP).
│ 
└── requirements.txt     # Liste des dépendances Python.
```

---

## 3. Dépendances

plaintext
Copier le code
flask
flet
hl7
lxml
paramiko
pywin32
pyjwt
pytest

---

## 4. Étapes principales

1.	Configuration :
- Créez settings.py pour stocker les paramètres comme les ports et les identifiants SFTP.
2.	Interface graphique :
- Construisez une interface utilisateur intuitive avec Flet.
3.	Traitement des fichiers :
- Implémentez des fonctions robustes pour lire, modifier et valider les formats HL7, HPRIM XML et CSV.
4.	Transmission :
- Développez des classes pour gérer les connexions TCP/IP et SFTP.
5.	Authentification :
- Ajoutez des fonctionnalités de login/logout et des protections JWT.
6.	Déploiement :
- Configurez l'application pour tourner comme un service sous Windows.
Si vous souhaitez que je développe des parties spécifiques ou fournisse des exemples de code, faites-le-moi savoir !

 
Phase 1 : Analyse et planification (1 semaine)
Objectifs :
- Définir clairement les besoins fonctionnels et techniques.
- Identifier les ressources nécessaires (bibliothèques, outils, compétences).
- Valider l'architecture logicielle et l'arborescence des fichiers.
Tâches :
- Analyser les formats HL7, HPRIM XML, et CSV pour identifier les règles de traitement spécifiques.
- Décider des détails d'implémentation des protocoles TCP/IP et SFTP.
- Rédiger des spécifications techniques pour les modules :
	- Gestion des fichiers.
	- Transmission.
	- Authentification.
	- Interface utilisateur.
- Créer une maquette de l'interface utilisateur avec Flet.

Phase 2 : Mise en place des bases de l'application (2 semaines)
Objectifs :
- Préparer l'infrastructure logicielle de l'application.
- Implémenter les fonctionnalités fondamentales.
Tâches :
- Initialisation du projet :
	- Configurer le dépôt Git (GitHub, GitLab, etc.).
	- Créer la structure de fichiers et installer les dépendances via requirements.txt.
- Configuration :
	- Implémenter les paramètres réseau et les configurations dans settings.py.
	- Ajouter un fichier de configuration pour les logs.
- Backend de traitement des fichiers :
	- Implémenter les modules hl7_processor.py, hprim_processor.py, et csv_processor.py.
	- Créer des fonctions de test unitaire pour chaque module.
- Transmission :
	- Développer et tester l'envoi/réception de données en TCP/IP.
	- Configurer un environnement SFTP pour tester la transmission des fichiers.
- Authentification :
	- Ajouter l'authentification avec JWT dans auth.py et tester les routes d'authentification.

Phase 3 : Développement avancé (3 semaines)
Objectifs :
- Ajouter des fonctionnalités secondaires.
- Développer et tester l'interface utilisateur.
Tâches :
- Interface graphique :
	- Créer une interface utilisateur interactive avec Flet (interface.py).
	- Ajouter des fonctionnalités pour :
		- Visualiser les fichiers reçus.
		- Modifier les configurations réseau (port TCP, SFTP, etc.).
- Service Windows :
	- Implémenter le service Windows avec pywin32 (service_manager.py).
	- Tester le démarrage, l'arrêt et la gestion du service.
- Traitement des erreurs :
	- Ajouter une gestion robuste des erreurs pour les modules de traitement de fichiers.
	- Loguer les erreurs critiques (HL7 mal formé, échec de connexion TCP/SFTP).
- Tests :
	- Écrire des tests pour tous les modules dans le dossier tests/.
	- Tester les fonctionnalités de bout en bout (reception -> modification -> émission).

Phase 4 : Validation et déploiement (2 semaines)
Objectifs :
- Tester l'application dans un environnement réel.
- Préparer la documentation et les guides d’utilisation.
Tâches :
- Tests finaux :
	- Tester l'application sur un serveur Windows.
	- Valider les transmissions TCP/IP et SFTP avec des données réelles.
	- Effectuer des tests de charge pour évaluer les performances.
- Documentation :
	- Documenter le code (docstrings, commentaires).
	- Rédiger un guide utilisateur pour l'interface.
	- Créer un guide d'installation et de configuration.
- Déploiement :
	- Packager l'application pour un déploiement facile (fichier EXE ou script d’installation).
	- Configurer le service sur le serveur Windows de production.

Phase 5 : Maintenance et améliorations continues (ongoing)
Objectifs :
- Ajouter des fonctionnalités basées sur les retours d'utilisateurs.
- Corriger les bogues et optimiser l'application.
Tâches :
- Mettre en place un système de tickets pour le suivi des bugs et des améliorations.
- Ajouter des fonctionnalités supplémentaires, comme :
	- Envoi automatique des notifications en cas d'échec de transmission.
	- Intégration avec des bases de données pour stocker les logs.
	- Export des fichiers traités dans d'autres formats.
- Planifier des mises à jour régulières pour suivre l’évolution des formats HL7 et HPRIM.


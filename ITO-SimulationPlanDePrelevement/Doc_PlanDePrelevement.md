# Documentation Technique de l'Application HL7

## Introduction

Cette application implémente un système de communication basé sur le protocole HL7 (Health Level 7), un standard utilisé dans le domaine de la santé pour l'échange d'informations médicales. L'application est conçue pour recevoir, transformer et envoyer des messages HL7 entre un client et un serveur. Elle utilise le protocole MLLP (Minimal Lower Layer Protocol) pour la communication réseau et permet la transformation de certains segments HL7 en fonction des règles métiers.

L'application se compose de plusieurs modules interconnectés, chacun ayant une responsabilité spécifique dans le processus de gestion des messages HL7.

## Architecture

L'application est structurée autour de plusieurs composants clés :

1. **Server (serveur HL7)** : Reçoit des messages HL7 entrants via une connexion réseau, traite ces messages, puis les envoie après transformation.
2. **Receiver (receveur)** : Reçoit les messages HL7 provenant d'autre système HL7.
3. **Transformer** : Modifie les segments des messages HL7 en fonction de règles spécifiées (ex. échange de certains champs entre émetteur et récepteur).
4. **Sender (expéditeur)** : Envoie les messages HL7 transformés vers un autre système HL7.
5. **Configuration** : Gestion de la configuration du serveur, incluant l'adresse du serveur cible, les ports d'entrée/sortie, et la verbosité des logs.
6. **Routeur** : Permet de naviguer dans l'application avec un système de routes basé sur la bibliothèque `Flet`.

---

## Composants

### 1. `hl7Server.py`

**Responsabilité** : Gère la réception des messages HL7 via une connexion MLLP et leur envoi après transformation.

**Fonctionnement** :
- Le serveur est démarré via la fonction `startServer()`, qui écoute sur un port spécifique configuré dans un fichier `config.txt`.
- Lorsqu'un message HL7 est reçu, il est traité par la fonction `messageReceiver()`, qui extrait les segments, les affiche, puis envoie un accusé de réception (ACK).
- Après avoir reçu le message, il est transmis à la fonction `transform_message()` pour transformation, puis envoyé à un autre serveur via la fonction `messageSender()`.

---

### 2. `hl7Receiver.py`

**Responsabilité** : Reçoit les messages HL7 via la connexion MLLP et leur accorde un accusé de réception.

**Fonctionnement** :
- La fonction `messageReceiver()` est appelée chaque fois qu'une connexion est établie avec le serveur HL7. Elle lit les messages HL7 entrants, les affiche, puis envoie un ACK (Acknowledgment) au client.
- Le message reçu est ensuite transformé par la fonction `transform_message()`, avant d'être renvoyé à un autre système via la fonction `messageSender()`.

---

### 3. `hl7Sender.py`

**Responsabilité** : Envoie des messages HL7 à un serveur de réception.

**Fonctionnement** :
- La fonction `messageSender()` est responsable de la connexion au serveur cible via MLLP. Elle envoie le message HL7 transformé et attend un accusé de réception (ACK).
- L'adresse du serveur cible, ainsi que le port de réception, sont lus à partir du fichier de configuration.

---

### 4. `hl7Transformer.py`

**Responsabilité** : Modifie les segments HL7 selon les règles spécifiées.

**Fonctionnement** :
- Le message HL7 reçu est passé à la fonction `transform_message()`, qui extrait chaque segment du message et applique des modifications spécifiques sur certains champs (ex. échange de l'émetteur et du récepteur dans le segment MSH).
- La fonction retourne le message transformé sous forme de liste de segments.

---

### 5. `config.py`

**Responsabilité** : Lecture et écriture de la configuration du serveur.

**Fonctionnement** :
- Le fichier `config.txt` contient les paramètres nécessaires pour configurer le serveur : l'adresse du serveur cible, le port d'entrée, le port de sortie et le mode de service.
- Les fonctions `readConf()` et `writeConf()` permettent de lire et de modifier ces paramètres.

---

### 6. `router.py`

**Responsabilité** : Gère la navigation de l'application via un système de routes.

**Fonctionnement** :
- Le `Router` permet de gérer les vues de l'application en fonction de l'URL demandée. Il utilise la bibliothèque `Flet` pour construire des interfaces utilisateur dynamiques.
- Lorsqu'une route est changée, la fonction `route_change()` met à jour le contenu de la page en fonction de la route.

---

## Fonctionnalités

### Réception de messages HL7
- Le serveur attend les messages HL7 entrants sur un port spécifié. Lorsqu'un message est reçu, il est analysé et un accusé de réception (ACK) est envoyé.

### Transformation des messages HL7
- Les messages HL7 sont transformés selon des règles prédéfinies, telles que l'échange de certains champs entre les segments MSH, PID, ORC, etc.

### Envoi des messages HL7 transformés
- Une fois le message transformé, il est envoyé à un autre serveur HL7 en utilisant le protocole MLLP. Le serveur attend un accusé de réception.

### Configuration
- La configuration du serveur est gérée à partir d'un fichier texte, où sont définis les paramètres nécessaires à la connexion au serveur cible et aux ports utilisés.

---

## Conclusion

L'application permet de recevoir, transformer et envoyer des messages HL7 tout en offrant une gestion flexible de la configuration via un fichier texte. Grâce à la modularité de son architecture, elle est facilement extensible pour intégrer de nouvelles règles de transformation ou de nouveaux segments HL7.

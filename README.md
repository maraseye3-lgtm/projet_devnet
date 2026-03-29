# NetMon - Projet d'Examen DEVNET (L3 RI)

Ce projet est une application de monitoring réseau développée avec Flask, PostgreSQL et Docker. Il permet de surveiller l'état (en ligne/hors ligne) et la latence de divers équipements réseau en temps réel.

## 1. Objectif du Projet
Résoudre le problème de la surveillance proactive des équipements réseau. L'application permet d'ajouter des adresses IP ou des noms de domaine et de suivre leur disponibilité via un tableau de bord web.

## 2. Architecture du Système
L'architecture est composée de trois services principaux orchestrés par Docker Compose :
- **Service Web (Flask)** : Fournit l'interface utilisateur et l'API REST.
- **Service de Monitoring (Python Worker)** : Effectue des tests de ping réguliers sur les équipements enregistrés en base de données.
- **Base de données (PostgreSQL)** : Stocke la liste des équipements, leur statut actuel, leur latence et l'historique de disponibilité.

## 3. Aspect Réseau
- **Communication Inter-Conteneurs** : Utilisation d'un réseau Docker (`netmon-network`) permettant aux services `app` et `monitor` de communiquer avec le service `db` via des noms d'hôtes DNS internes.
- **Monitoring Réseau** : Le service worker utilise le protocole ICMP (ping) pour vérifier la connectivité réseau vers des cibles externes (ex: Google DNS, sites web, etc.).

## 4. Technologies Utilisées
- **Backend** : Flask, Flask-SQLAlchemy, Psycopg2
- **Monitoring** : Subprocess (Ping), Python
- **Base de Données** : PostgreSQL
- **Conteneurisation** : Docker, Docker Compose
- **CI/CD** : GitHub Actions
- **Frontend** : HTML5, CSS3, JavaScript (Vanilla)

## 5. Installation et Exécution

### Prérequis
- Docker et Docker Compose installés sur votre machine.

### Lancement du projet
1. Clonez le dépôt GitHub.
2. Lancez les services avec Docker Compose :
   ```bash
   docker-compose up --build
   ```
3. Accédez à l'application via votre navigateur à l'adresse : `http://localhost:5000`

## 6. CI/CD
Le projet inclut un pipeline GitHub Actions qui :
1. Se déclenche à chaque push sur la branche `main`.
2. Construit les images Docker pour l'application et le worker.
3. Publie les images sur Docker Hub.

## 7. Support de Présentation (Points clés)
- **Problème résolu** : Difficulté de surveiller manuellement plusieurs équipements réseau.
- **Démonstration** : 
  - Ajout d'un équipement (ex: `8.8.8.8`).
  - Visualisation du changement de statut dans le tableau de bord.
  - Vérification des conteneurs en cours d'exécution via `docker ps`.
  - Vérification de la communication réseau via `docker logs netmon_monitor`.

---
**Étudiant** : [Serigne Mouhamadou Moctar Seye]
**Établissement** : ISI Keur Massar
**Classe** : Licence 3 Réseaux et Informatique (L3 RI)

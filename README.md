# PRO CHEZ NOUS

PRO CHEZ NOUS est une plateforme qui met en relation des clients et des professionnels de services et de métiers manuels. Les clients peuvent rechercher des professionnels, consulter leur profil et demander des rendez-vous ou des devis.

## Fonctionnalités

- Inscription et connexion pour les clients et les professionnels
- Recherche de professionnels par métier et localisation
- Gestion des disponibilités et réservation de rendez-vous
- Avis et évaluations
- Demandes et réponses aux devis
- Messagerie et favoris
- Profils professionnels et vérification de documents
- Abonnements gratuits et Premium
- Espace d’administration pour les utilisateurs, les catégories, les vérifications et les commerciaux
- Intégrations prévues pour FedaPay, l’envoi d’e-mails et les SMS; leur disponibilité dépend de la configuration des services

## Technologies

- Python et Flask
- SQLite
- Modèles HTML avec Jinja2, CSS et JavaScript
- Gunicorn pour servir l’application
- FedaPay, SendGrid et Twilio en option

## Lancer l’application localement

Prérequis : Python 3 et `pip`.

```bash
git clone https://github.com/Gkconsulting20/Procheznous.git
cd Procheznous
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

L’application est ensuite disponible à l’adresse `http://127.0.0.1:5000`.

Sous Windows, activez l’environnement virtuel avec `.venv\Scripts\activate` avant d’installer les dépendances.

## Configuration

En production, définissez une valeur secrète forte pour `SECRET_KEY`. Les variables pour FedaPay, SendGrid et Twilio sont facultatives et sont listées dans [`.env.example`](.env.example). Configurez les vraies valeurs dans l’environnement d’exécution ou dans le gestionnaire de secrets de l’hébergeur; ne publiez pas de clés réelles dans GitHub.

La base de données utilisée par l’application est SQLite (`database.db`). Le lancement avec `python app.py` appelle l’initialisation de la base prévue dans l’application.

## Déploiement

Le dépôt contient plusieurs guides de déploiement, notamment pour PythonAnywhere :

- [`GUIDE_DEPLOIEMENT_PYTHONANYWHERE.md`](GUIDE_DEPLOIEMENT_PYTHONANYWHERE.md)
- [`DEPLOIEMENT_FINAL_PYTHONANYWHERE.md`](DEPLOIEMENT_FINAL_PYTHONANYWHERE.md)

Pour lancer l’application avec Gunicorn :

```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

## Documents utiles

- [`FORMATION_COMMERCIAUX_PRO_CHEZ_NOUS.md`](FORMATION_COMMERCIAUX_PRO_CHEZ_NOUS.md) — support de formation commerciale
- [`MON_SUIVI_PRO_CHEZ_NOUS.md`](MON_SUIVI_PRO_CHEZ_NOUS.md) — résumé de suivi du projet
- [`MODELE_COMMERCIALISATION.md`](MODELE_COMMERCIALISATION.md) — modèle de commercialisation

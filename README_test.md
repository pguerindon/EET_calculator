# EET Calculator

**Version : 1.10** **Auteur : Philippe Guérindon**

## Présentation

EET Calculator est une application web permettant de calculer un **Temps
Électronique Équivalent (Equivalent Electronic Time - EET)**
conformément aux règles de chronométrage de la **Fédération
Internationale de Ski (FIS)**.

L'application permet de déterminer le temps électronique manquant d'un
concurrent à partir des temps électroniques et manuels des concurrents
précédents.

Le calcul est effectué en **microsecondes** afin de garantir la
précision maximale avant l'arrondi à la précision souhaitée.

------------------------------------------------------------------------

## Fonctionnalités

- Calcul du Temps Électronique Équivalent (EET).

- Conforme aux règles FIS.

- Interface responsive (PC, tablette et smartphone).

- Gestion multilingue :

  - Français
  - English
  - Deutsch

- Génération d'un rapport PDF.

- Historique des deux derniers calculs.

- Persistance des calculs pendant toute la session utilisateur.

- Fonction **Recharger** permettant de permuter les deux derniers
  calculs.

------------------------------------------------------------------------

## Architecture

    run.py
        │
        ▼
    app.py
        │
        ├── services/
        │      ├── formulaire.py
        │      ├── eet_calculator.py
        │      ├── eet.py
        │      ├── temps.py
        │      └── views.py
        │
        ├── pdf.py
        ├── translation.py
        └── config.py

### Description des modules

  -------------------------------------------------------------------
  Module                       Rôle
  ---------------------------- --------------------------------------
  app.py                       Routes Flask et orchestration de
                               l'application

  config.py                    Paramètres généraux de l'application

  translation.py               Gestion des traductions

  pdf.py                       Génération des rapports PDF

  services/formulaire.py       Lecture et initialisation du
                               formulaire

  services/eet_calculator.py   Orchestration du calcul EET

  services/eet.py              Algorithmes de calcul EET

  services/temps.py            Manipulation des temps et conversions

  services/views.py            Affichage des pages HTML
  -------------------------------------------------------------------

------------------------------------------------------------------------

## Installation

### Prérequis

- Python 3.12 ou supérieur
- pip
- python3-venv

### Installation

    python -m venv venv

Activation de l'environnement virtuel :

Linux :

    source venv/bin/activate

Windows :

    venv\Scripts\activate

Installation des dépendances :

    pip install -r requirements.txt

------------------------------------------------------------------------

## Lancement

Développement :

    python run.py

L'application est alors accessible à l'adresse :

    http://localhost:5000

------------------------------------------------------------------------

## Déploiement

En production, l'application est prévue pour fonctionner avec :

- Gunicorn
- Nginx (ou Apache en reverse proxy)

Consulter les documents présents dans le dossier **Documentation/** pour
les procédures complètes de déploiement.

------------------------------------------------------------------------

## Structure du projet

    app.py
    config.py
    pdf.py
    run.py
    translation.py
    requirements.txt

    services/
    templates/
    static/
    tests/
    Documentation/

------------------------------------------------------------------------

## Tests

Les fonctions de calcul sont indépendantes de l'interface Flask et
peuvent être testées séparément.

Le dossier **tests/** contient les scripts de validation du moteur de
calcul.

------------------------------------------------------------------------

## Licence

Application développée par Philippe Guérindon.

Tous droits réservés.

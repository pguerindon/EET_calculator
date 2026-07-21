from flask import (
    request,
    session,
)

from config import (
    DEFAULT_LANGUAGE,
    SUPPORTED_LANGUAGES,
)

TEXTES = {

    "fr": {

        #
        # Interface principale
        #

        "home_title": "EET Calculator - Calculateur EET pour le ski alpin",
        "calcul_precedent": "Calcul précédent",
        "calculer": "Calculer EET",
        "correction": "Somme Delta / 10",
        "delta": "Delta",
        "dossard": "Dossard",
        "dossard_eet": "Dossard EET",
        "eet_calculee": "EET calculé",
        "effacer": "Effacer",
        "erreur_aucun_te": "Erreur : aucun temps électronique à calculer.",
        "erreur_plusieurs_te": "Erreur : plusieurs temps électroniques manquants.",
        "erreur_references": "Erreur : 10 références complètes sont nécessaires.",
        "erreur_tm": "Erreur : tous les temps manuels (TOD) doivent être renseignés.",
        "exemple_fis": "Exemple FIS",
        "grille_valide": "Grille valide",
        "langue": "Langue",
        "pdf": "PDF",
        "nom_pdf": "Calcul_EET",
        "precision_te": "Précision TE",
        "precision_tm": "Précision TM",
        "recharger": "Recharger",
        "references": "Références",
        "resultat": "Résultat",
        "resultat_sous_grille": "Résultat sous la grille",
        "retour": "Retour",
        "somme_delta": "Somme Delta",
        "te": "TE (TOD)",
        "temps_electronique": "Temps électronique (TOD)",
        "temps_manuel": "Temps manuel (TOD)",
        "titre": "Calculateur EET",
        "tm": "TM (TOD)",
        "meta_description": "Calculateur EET (Equivalent Electronic Time) pour les compétitions de ski alpin. Calcul conforme aux règlements FIS et nationaux à partir des temps manuels ou du système B de chronométrage.",

        #
        # Recherche de calcul
        #

        "rechercher_calcul": "Rechercher un calcul",
        "saison": "Saison",
        "codex": "Codex",
        "rechercher": "Rechercher",
        "fermer": "Fermer",
        "discipline": "Discipline",
        "manche": "Manche",
        "date": "Date",
        "lieu": "Lieu",
        "consulter": "Consulter",
        "aucun_calcul_trouve": "Aucun calcul trouvé.",

        #
        # Lexique
        #

        "lexique_titre": "Lexique",
        "lexique_precision": "xxxxx",
        "lexique_precision_txt": "Précision des chronomètres.",
        "lexique_tm": "Temps manuel sous la forme heure du jour - hh:mm:ss.xxxxxxx",
        "lexique_te": "Temps électronique sous la forme heure du jour - hh:mm:ss.xxxxxxx",
        "lexique_eet": "Equivalent Electronic Time sous la forme heure du jour - hh:mm:ss.xxxxxxx",
        "lexique_precision_tm": "Précision TM",
        "lexique_precision_tm_txt": "Précision du chronomètre de saisie des TM.",
        "lexique_precision_te": "Précision TE",
        "lexique_precision_te_txt": "Précision du chronomètre de saisie des TE.",
        "lexique_tod": "Heure du jour",

        #
        # Aide
        #

        "aide": "Aide",
        "aide_title": "EET Calculator - Aide",
        "aide_calcul": "Calcul",
        "aide_calcul_l1a": "Cliquer sur ",
        "aide_calcul_l1b": "Calculer EET",
        "aide_calcul_l2": "L'application :",
        "aide_calcul_l3": "calcule les deltas TM − TE des 10 références ;",
        "aide_calcul_l4": "calcule la correction moyenne ;",
        "aide_calcul_l5": "applique cette correction au temps manuel (TOD) du concurrent concerné ;",
        "aide_calcul_l6": "affiche l'EET calculé.",
        "aide_calcul_explication_l1": "Si la somme des deltas est négative, les temps manuels (TM) sont globalement inférieurs aux temps électroniques (TE). Les doublages manuels sont alors « en avance » sur les temps électroniques. La correction calculée est négative et l'EET obtenue est supérieure au temps manuel (TM) du concurrent concerné.",
        "aide_calcul_explication_l2": "Inversement, si la somme des deltas est positive, les temps manuels sont globalement supérieurs aux temps électroniques. Les doublages manuels sont alors « en retard » sur les temps électroniques. La correction calculée est positive et l'EET obtenue est inférieure au temps manuel (TM) du concurrent concerné.",
        "aide_exemple_fis": "Exemple FIS",
        "aide_exemple_fis_l1a": "Le bouton ",
        "aide_exemple_fis_l1b": " charge l'exemple utilisé dans la documentation FIS afin de vérifier le fonctionnement de l'application.",
        "aide_precision_des_temps": "Précision des temps",
        "aide_precision_des_temps_l1": "Conformément au règlement, les calculs sont effectués dans la précision maximale des chronomètres.",
        "aide_precision_des_temps_l2": "Pour cette raison, l'application convertit les temps en microsecondes et réalise l'ensemble des calculs avec cette précision.",
        "aide_precision_des_temps_l3a": "Les paramètres ",
        "aide_precision_des_temps_l3b": " et ",
        "aide_precision_des_temps_l3c": " permettent uniquement de définir le nombre de décimales affichées et saisies.",
        "aide_precision_des_temps_l4": "Ils n'ont aucune influence sur la précision des calculs ni sur l'EET calculée.",
        "aide_principe": "Principe",
        "aide_principe_l1": "Le calcul de l'Equivalent Electronic Time (EET) permet de déterminer un temps électronique équivalent lorsqu'un concurrent ne dispose que d'un temps manuel (TOD).",
        "aide_principe_l2": "Le calcul nécessite : ",
        "aide_principe_l3": "11 concurrents ;",
        "aide_principe_l4": "10 concurrents de référence disposant d'un temps manuel (TOD) et d'un temps électronique (TOD);",
        "aide_principe_l5": "1 concurrent dont le temps électronique est absent.",
        "aide_rapport_pdf": "Rapport PDF",
        "aide_rapport_pdf_l1a": "Après calcul, le bouton ",
        "aide_rapport_pdf_l1b": "permet de générer un rapport contenant : ",
        "aide_rapport_pdf_l2": "les données saisies ;",
        "aide_rapport_pdf_l3": "les deltas des références ;",
        "aide_rapport_pdf_l4": "la correction calculée ;",
        "aide_rapport_pdf_l5": "l'EET obtenu ;",
        "aide_rapport_pdf_l6": "la date et l'heure du calcul.",
        "aide_saisie_des_donnees": "Saisie des données",
        "aide_saisie_des_donnees_l1": "Saisir les 11 dossards.",
        "aide_saisie_des_donnees_l2": "Saisir les temps manuels (TM - TOD) des 11 concurrents. Lorsqu'un système B de chronométrage est disponible, il est préférable d'utiliser les données du système B plutôt que les temps manuels.",
        "aide_saisie_des_donnees_l3": "Saisir les temps électroniques (TE - TOD) des 10 concurrents de référence.",
        "aide_saisie_des_donnees_l4": "Laisser vide le temps électronique (TOD) du concurrent à calculer.",
        "aide_saisie_des_donnees_l5a": "Vérifier que le message",
        "aide_saisie_des_donnees_l5b": "apparaît.",
        "aide_selection_des_references": "Sélection des références",
        "aide_selection_des_references_l1": "Pour le calcul de l'EET, l'application utilise toujours 10 concurrents de référence.",
        "aide_selection_des_references_l2": "Les références sont recherchées en priorité parmi les concurrents précédant le concurrent dont le temps électronique (TOD) est à calculer.",
        "aide_selection_des_references_l3": "Si moins de 10 concurrents précèdent ce concurrent, les concurrents suivants sont utilisés afin d'obtenir un total de 10 références.",
        "aide_selection_des_references_l4": "Le concurrent dont l'EET est calculé n'est jamais utilisé comme référence.",

        #
        # Session
        #

        "session_confidentialite": "La conservation des calculs est limitée au navigateur et à l'appareil utilisé. Les données ne sont pas enregistrées dans une base de données permanente.",
        "session_duree": "Ces informations sont conservées dans la session du navigateur pendant 8 heures après la dernière utilisation de l'application.",
        "session_fin": "Au-delà de ce délai, ou après suppression des données de navigation du navigateur, les calculs mémorisés sont automatiquement supprimés.",
        "session_intro": "Le calculateur mémorise automatiquement :",
        "session_ligne_1": "le dernier calcul effectué ;",
        "session_ligne_2": "le calcul précédent.",
        "session_titre": "Session utilisateur",

        #
        # Confidentialité
        #

        "confidentialite_titre": "Confidentialité",
        "confidentialite_intro": "L'application EET Calculator ne collecte aucune donnée personnelle.",
        "confidentialite_compte": "Aucun compte utilisateur n'est requis et aucune adresse électronique n'est demandée.",
        "confidentialite_session": "Les calculs effectués sont conservés uniquement dans la session du navigateur afin de permettre le rappel du dernier calcul et du calcul précédent. Ces informations sont automatiquement supprimées à l'expiration de la session.",
        "confidentialite_stockage": "Aucune base de données n'est utilisée et aucune trace des calculs réalisés n'est conservée sur le serveur.",
        "confidentialite_ip": "L'application n'enregistre pas les adresses IP des utilisateurs et n'effectue aucun suivi statistique ou publicitaire.",

        #
        # À propos
        #

        "a_propos_title": "EET Calculator - À propos",
        "a_propos": "À propos",
        "a_propos_developpement": "Développement :",
        "a_propos_fonction_l1": "EET Calculator est une application dédiée au calcul de l'Equivalent Electronic Time (EET), conformément aux règles de chronométrage de la Fédération Internationale de Ski (FIS).",
        "a_propos_fonction_l2": "Elle permet de calculer un temps électronique équivalent à partir des temps manuels et des temps électroniques, conformément aux règles de chronométrage utilisées lors des compétitions FIS et des fédérations nationales.",
        "a_propos_fonction_l3": "L'application intègre également une calculatrice horaire destinée aux opérations courantes de chronométrage (calculs d'heures, de durées et d'écarts).",
        "a_propos_contact": "Contact :",

        #
        # Calculatrice horaire
        #

        "timecalc_title": "EET Calculator - Calculatrice horaire",
        "calculatrice_horaire": "Calculatrice horaire",
        "timecalc_titre": "Calculatrice horaire",
        "timecalc_depart": "Heure de départ",
        "timecalc_arrivee": "Heure d'arrivée",
        "timecalc_temps": "Temps de course",
        "timecalc_precision_tod": "Précision TOD",
        "timecalc_precision_temps": "Précision temps",
        "timecalc_calculer": "Calculer",
        "timecalc_calcul_ok": "✓ Calcul réussi.",
        "timecalc_effacer": "Effacer",
        "timecalc_erreur_deux_valeurs": "Erreur : renseigner exactement deux valeurs.",
        "timecalc_erreur_arrivee": "Erreur : l'heure d'arrivée doit être postérieure à l'heure de départ.",
        "timecalc_erreur_negative": "Erreur : le calcul produit une heure négative.",
        "timecalc_erreur_tod": "Erreur : heure invalide.",
        "timecalc_erreur_duree": "Erreur : durée invalide.",

        "timecalc_aide_title": "EET Calculator - Aide - Calculatrice horaire",
        "timecalc_aide_titre": "Aide - Calculatrice horaire",
        "timecalc_aide_principe": "Principe",
        "timecalc_aide_principe_l1": "Saisir exactement deux des trois valeurs : heure de départ, heure d'arrivée ou temps de course. La troisième valeur est calculée automatiquement.",
        "timecalc_aide_saisie": "Saisie",
        "timecalc_aide_saisie_l1": "Saisir exactement deux des trois valeurs.",
        "timecalc_aide_saisie_l2": "Les séparateurs ':' et '.' sont ajoutés automatiquement pendant la saisie.",
        "timecalc_aide_saisie_l3": "Les heures sont saisies sous la forme hh:mm:ss.xxxxxx.",
        "timecalc_aide_saisie_l4": "Les temps de course sont saisis sous la forme hh:mm:ss.xxx.",
        "timecalc_aide_precision": "Précisions",
        "timecalc_aide_precision_l1": "La précision des heures de départ et d'arrivée (TOD) peut être choisie entre 3 et 6 décimales.",
        "timecalc_aide_precision_l2": "La précision du temps de course peut être choisie entre 2 et 3 décimales.",
        "timecalc_aide_precision_l3": "Tous les calculs sont effectués à la microseconde, quelle que soit la précision affichée.",
        "timecalc_aide_calcul": "Calcul",
        "timecalc_aide_calcul_l1": "La calculatrice peut effectuer les calculs suivants :",
        "timecalc_aide_calcul_l2": "Heure de départ + Heure d'arrivée → Temps de course",
        "timecalc_aide_calcul_l3": "Heure de départ + Temps de course → Heure d'arrivée",
        "timecalc_aide_calcul_l4": "Heure d'arrivée + Temps de course → Heure de départ",
        "timecalc_aide_remarques": "Remarques",
        "timecalc_aide_remarques_l1": "Lorsque le temps de course est calculé, le résultat est tronqué à la précision sélectionnée et n'est jamais arrondi.",
        "timecalc_aide_remarques_l2": "Les heures de départ et d'arrivée doivent être comprises entre 00:00:00 et 23:59:59.",
        "timecalc_aide_remarques_l3": "Les minutes et les secondes doivent être inférieures à 60.",
        "timecalc_aide_remarques_l4": "Les données saisies ne sont pas conservées après avoir quitté la page.",
        "timecalc_aide_exemples": "Exemples",
        "timecalc_aide_ex1": "Calcul du temps de course",
        "timecalc_aide_ex1_l1": "Heure de départ : 10:00:00.000000",
        "timecalc_aide_ex1_l2": "Heure d'arrivée : 10:01:12.345678",
        "timecalc_aide_ex1_l3": "Résultat : 00:01:12.34",
        "timecalc_aide_ex2": "Calcul de l'heure d'arrivée",
        "timecalc_aide_ex2_l1": "Heure de départ : 10:00:00.000000",
        "timecalc_aide_ex2_l2": "Temps de course : 00:01:12.34",
        "timecalc_aide_ex2_l3": "Résultat : 10:01:12.340000",
        "timecalc_aide_ex3":  "Calcul de l'heure de départ",
        "timecalc_aide_ex3_l1": "Heure d'arrivée : 10:01:12.340000",
        "timecalc_aide_ex3_l2": "Temps de course : 00:01:12.34",
        "timecalc_aide_ex3_l3": "Résultat : 10:00:00.000000",
        "timecalc_aide_remarque_l1": "Tous les calculs sont effectués à la microseconde.",
        "timecalc_aide_remarque_l2": "Lorsque le temps de course est calculé, le résultat est tronqué à la précision sélectionnée et n'est jamais arrondi.",
        "timecalc_aide_remarque_l3": "Les heures de départ et d'arrivée doivent être comprises entre 00:00:00 et 23:59:59.",        
        "erreurs": 
            {"dossard_eet_absent": "Aucun dossard EET n'a été sélectionné.",
            "dossard_eet_inconnu": "Le dossard EET n'existe pas.",
            "temps_manuel_absent": "Le temps manuel est absent.",
            "temps_electronique_absent": "Le temps électronique est absent.",
            },

        #
        # Pdf
        #

        "pdf_title": "Calcul du temps électronique équivalent (EET)",
        "date_calcul": "Date du calcul",
        "calculation_id": "Id du calcul",
        "departure": "Départ",
        "arrival": "Arrivée",
        "missing_impulse": "Impulsion manquante",
        "eet_bib": "Dossard EET",
        "location": "Station",
    },

    "en": {

        #
        # Interface principale
        #

        "home_title": "EET Calculator - Equalized Equivalent Time Calculator for Alpine Skiing",
        "calcul_precedent": "Previous calculation",
        "calculer": "Calculate EET",
        "correction": "Delta Sum / 10",
        "delta": "Delta",
        "dossard": "Bib",
        "dossard_eet": "EET Bib",
        "eet_calculee": "Calculated EET",
        "effacer": "Clear",
        "erreur_aucun_te": "Error: no electronic time to calculate.",
        "erreur_plusieurs_te": "Error: several electronic times are missing.",
        "erreur_references": "Error: 10 complete reference times are required.",
        "erreur_tm": "Error: all manual times (TOD) must be entered.",
        "exemple_fis": "FIS Example",
        "grille_valide": "Valid grid",
        "langue": "Language",
        "pdf": "PDF",
        "nom_pdf": "EET_Calculation",
        "precision_te": "ET Precision",
        "precision_tm": "MT Precision",
        "recharger": "Reload",
        "references": "References",
        "resultat": "Result",
        "resultat_sous_grille": "Result below the grid",
        "retour": "Back",
        "somme_delta": "Delta Sum",
        "te": "ET (TOD)",
        "temps_electronique": "Electronic time (TOD)",
        "temps_manuel": "Manual time (TOD)",
        "titre": "EET Calculator",
        "tm": "MT (TOD)",
        "meta_description": "EET Calculator (Equivalent Electronic Time) for alpine skiing competitions. Compute replacement electronic times according to FIS and national timing procedures using manual timing or timing system B data.",

        #
        # Calculation search
        #

        "rechercher_calcul": "Search for a calculation",
        "saison": "Season",
        "codex": "Codex",
        "rechercher": "Search",
        "fermer": "Close",
        "discipline": "Discipline",
        "manche": "Run",
        "date": "Date",
        "lieu": "Location",
        "consulter": "View",
        "aucun_calcul_trouve": "No calculation found.",

        #
        # Glossary
        #

        "lexique_titre": "Glossary",
        "lexique_precision": "xxxxx",
        "lexique_precision_txt": "Timer precision.",
        "lexique_tm": "Manual Time in time-of-day format - hh:mm:ss.xxxxxxx",
        "lexique_te": "Electronic Time in time-of-day format - hh:mm:ss.xxxxxxx",
        "lexique_eet": "Equivalent Electronic Time in time-of-day format - hh:mm:ss.xxxxxxx",
        "lexique_precision_tm": "MT Precision",
        "lexique_precision_tm_txt": "Precision of the timer used for Manual Time entry.",
        "lexique_precision_te": "ET Precision",
        "lexique_precision_te_txt": "Precision of the timer used for Electronic Time entry.",
        "lexique_tod": "Time Of Day", 

        #
        # Aide
        #

        "aide": "Help",
        "aide_title": "EET Calculator - Help",
        "aide_calcul": "Calculation",
        "aide_calcul_l1a": "Click ",
        "aide_calcul_l1b": "Calculate EET",
        "aide_calcul_l2": "The application:",
        "aide_calcul_l3": "calculates the MT − ET deltas of the 10 references;",
        "aide_calcul_l4": "calculates the average correction;",
        "aide_calcul_l5": "applies this correction to the competitor's manual time (TOD);",
        "aide_calcul_l6": "displays the calculated EET.",
        "aide_calcul_explication_l1": "If the sum of the deltas is negative, the manual times (MT) are generally lower than the electronic times (ET). The manual backup times are therefore 'ahead' of the electronic times. The calculated correction is negative and the resulting EET is greater than the competitor's manual time (MT).",
        "aide_calcul_explication_l2": "Conversely, if the sum of the deltas is positive, the manual times are generally higher than the electronic times. The manual backup times are therefore 'behind' the electronic times. The calculated correction is positive and the resulting EET is lower than the competitor's manual time (MT).",
        "aide_exemple_fis": "FIS Example",
        "aide_exemple_fis_l1a": "The ",
        "aide_exemple_fis_l1b": " button loads the example used in the FIS documentation in order to verify the application's operation.",
        "aide_precision_des_temps": "Time Precision",
        "aide_precision_des_temps_l1": "In accordance with the regulations, calculations are performed using the maximum precision of the timing devices.",
        "aide_precision_des_temps_l2": "For this reason, the application converts times into microseconds and performs all calculations using this precision.",
        "aide_precision_des_temps_l3a": "The ",
        "aide_precision_des_temps_l3b": " and ",
        "aide_precision_des_temps_l3c": " settings are used only to define the number of displayed and entered decimal places.",
        "aide_precision_des_temps_l4": "They have no influence on the precision of the calculations or on the calculated EET.",
        "aide_principe": "Principle",
        "aide_principe_l1": "The Equivalent Electronic Time (EET) calculation makes it possible to determine an equivalent electronic time when a competitor only has a manual time (TOD).",
        "aide_principe_l2": "The calculation requires:",
        "aide_principe_l3": "11 competitors;",
        "aide_principe_l4": "10 reference competitors with both a manual time (TOD) and an electronic time (TOD);",
        "aide_principe_l5": "1 competitor whose electronic time is missing.",
        "aide_rapport_pdf": "PDF Report",
        "aide_rapport_pdf_l1a": "After calculation, the ",
        "aide_rapport_pdf_l1b": " button generates a report containing:",
        "aide_rapport_pdf_l2": "the entered data;",
        "aide_rapport_pdf_l3": "the reference deltas;",
        "aide_rapport_pdf_l4": "the calculated correction;",
        "aide_rapport_pdf_l5": "the calculated EET;",
        "aide_rapport_pdf_l6": "the date and time of the calculation.",
        "aide_saisie_des_donnees": "Data Entry",
        "aide_saisie_des_donnees_l1": "Enter the 11 bib numbers.",
        "aide_saisie_des_donnees_l2": "Enter the manual times (MT - TOD) for the 11 competitors. When a timing System B is available, it is preferable to use the System B data rather than the manual times.",
        "aide_saisie_des_donnees_l3": "Enter the electronic times (ET - TOD) of the 10 reference competitors.",
        "aide_saisie_des_donnees_l4": "Leave blank the electronic time of the competitor to be calculated.",
        "aide_saisie_des_donnees_l5a": "Verify that the message",
        "aide_saisie_des_donnees_l5b": "is displayed.",
        "aide_selection_des_references": "Reference Selection",
        "aide_selection_des_references_l1": "The EET calculation always uses 10 reference competitors.",
        "aide_selection_des_references_l2": "References are selected first from the competitors preceding the competitor whose electronic time (TOD) is to be calculated.",
        "aide_selection_des_references_l3": "If fewer than 10 competitors precede this competitor, the following competitors are used to reach a total of 10 references.",
        "aide_selection_des_references_l4": "The competitor whose EET is being calculated is never used as a reference.",

        #
        # Session
        #

        "session_confidentialite": "Calculations are stored only in the browser and on the device being used. No data is stored in a permanent database.",
        "session_duree": "This information is stored in the browser session for 8 hours after the last use of the application.",
        "session_fin": "After this period, or if the browser data is cleared, the stored calculations are automatically deleted.",
        "session_intro": "The calculator automatically stores:",
        "session_ligne_1": "the last calculation performed;",
        "session_ligne_2": "the previous calculation.",
        "session_titre": "User session",

        #
        # Confidentialité
        #

        "confidentialite_titre": "Privacy",
        "confidentialite_intro": "The EET Calculator application does not collect any personal data.",
        "confidentialite_compte": "No user account is required and no email address is requested.",
        "confidentialite_session": "Calculations are stored only in the browser session to allow retrieval of the last calculation and the previous calculation. This information is automatically deleted when the session expires.",
        "confidentialite_stockage": "No database is used and no record of the calculations performed is stored on the server.",
        "confidentialite_ip": "The application does not record users' IP addresses and does not perform any statistical or advertising tracking.",        

        #
        # About
        #

        "a_propos_title": "EET Calculator - About",
        "a_propos": "About",
        "a_propos_developpement": "Development:",
        "a_propos_fonction_l1": "EET Calculator is dedicated to the calculation of the Equivalent Electronic Time (EET) in accordance with the timing rules of the International Ski and Snowboard Federation (FIS).",
        "a_propos_fonction_l2": "It calculates an Equivalent Electronic Time from manual and electronic times, in accordance with the timing rules used during FIS and national federation competitions.",
        "a_propos_fonction_l3": "The application also includes a time calculator designed for everyday timing operations (time-of-day, duration and time difference calculations).",
        "a_propos_contact": "Contact:",

        #
        # Time Calculator
        #

        "timecalc_title": "EET Calculator - Time Calculator",
        "calculatrice_horaire": "Time Calculator",
        "timecalc_titre": "Time Calculator",
        "timecalc_depart": "Start Time",
        "timecalc_arrivee": "Finish Time",
        "timecalc_temps": "Elapsed Time",
        "timecalc_precision_tod": "TOD Precision",
        "timecalc_precision_temps": "Time Precision",

        "timecalc_calculer": "Calculate",
        "timecalc_effacer": "Clear",
        "timecalc_calcul_ok": "✓ Calculation successful.",
        "timecalc_erreur_deux_valeurs": "Error: enter exactly two values.",
        "timecalc_erreur_arrivee": "Error: finish time must be later than start time.",
        "timecalc_erreur_negative": "Error: calculation results in a negative time.",
        "timecalc_erreur_tod": "Error: invalid time of day.",
        "timecalc_erreur_duree": "Error: invalid elapsed time.",

        "timecalc_aide_title": "EET Calculator - Help - Time Calculator",
        "timecalc_aide_titre": "Help - Time Calculator",
        "timecalc_aide_principe": "Principle",
        "timecalc_aide_principe_l1": "Enter exactly two of the three values: start time, finish time or elapsed time. The third value is calculated automatically.",

        "timecalc_aide_saisie": "Input",
        "timecalc_aide_saisie_l1": "Enter exactly two of the three values.",
        "timecalc_aide_saisie_l2": "The ':' and '.' separators are inserted automatically while typing.",
        "timecalc_aide_saisie_l3": "Times of day are entered in the format hh:mm:ss.xxxxxx.",
        "timecalc_aide_saisie_l4": "Elapsed times are entered in the format hh:mm:ss.xxx.",

        "timecalc_aide_precision": "Precision",
        "timecalc_aide_precision_l1": "The precision of start and finish times (TOD) can be selected from 3 to 6 decimal places.",
        "timecalc_aide_precision_l2": "The precision of elapsed time can be selected from 2 to 3 decimal places.",
        "timecalc_aide_precision_l3": "All calculations are performed to the microsecond, regardless of the displayed precision.",

        "timecalc_aide_calcul": "Calculation",
        "timecalc_aide_calcul_l1": "The calculator can perform the following calculations:",
        "timecalc_aide_calcul_l2": "Start Time + Finish Time → Elapsed Time",
        "timecalc_aide_calcul_l3": "Start Time + Elapsed Time → Finish Time",
        "timecalc_aide_calcul_l4": "Finish Time + Elapsed Time → Start Time",

        "timecalc_aide_remarques": "Notes",
        "timecalc_aide_remarques_l1": "When elapsed time is calculated, the result is truncated to the selected precision and is never rounded.",
        "timecalc_aide_remarques_l2": "Start and finish times must be between 00:00:00 and 23:59:59.",
        "timecalc_aide_remarques_l3": "Minutes and seconds must be less than 60.",
        "timecalc_aide_remarques_l4": "Entered data is not retained after leaving the page.",

        "timecalc_aide_exemples": "Examples",

        "timecalc_aide_ex1": "Elapsed Time Calculation",
        "timecalc_aide_ex1_l1": "Start Time: 10:00:00.000000",
        "timecalc_aide_ex1_l2": "Finish Time: 10:01:12.345678",
        "timecalc_aide_ex1_l3": "Result: 00:01:12.34",

        "timecalc_aide_ex2": "Finish Time Calculation",
        "timecalc_aide_ex2_l1": "Start Time: 10:00:00.000000",
        "timecalc_aide_ex2_l2": "Elapsed Time: 00:01:12.34",
        "timecalc_aide_ex2_l3": "Result: 10:01:12.340000",

        "timecalc_aide_ex3": "Start Time Calculation",
        "timecalc_aide_ex3_l1": "Finish Time: 10:01:12.340000",
        "timecalc_aide_ex3_l2": "Elapsed Time: 00:01:12.34",
        "timecalc_aide_ex3_l3": "Result: 10:00:00.000000",

        "timecalc_aide_remarque_l1": "All calculations are performed to the microsecond.",
        "timecalc_aide_remarque_l2": "When elapsed time is calculated, the result is truncated to the selected precision and is never rounded.",
        "timecalc_aide_remarque_l3": "Start and finish times must be between 00:00:00 and 23:59:59.",

        "erreurs": {
            "dossard_eet_absent": "No EET bib has been selected.",
            "dossard_eet_inconnu": "The EET bib does not exist.",
            "temps_manuel_absent": "The manual time is missing.",
            "temps_electronique_absent": "The electronic time is missing.",
        },

        #
        # Pdf
        #

        "pdf_title": "Equivalent Electronic Time (EET) Calculation",
        "date_calcul": "Calculation date",
        "calculation_id": "Calculation ID",
        "departure": "Start",
        "arrival": "Finish",
        "missing_impulse": "Missing impulse",
        "eet_bib": "EET Bib",
        "location": "Location",

    },

    "de": {

        #
        # Interface principale
        #

        "home_title": "EET Calculator - EET-Rechner für alpine Skirennen",
        "calcul_precedent": "Vorherige Berechnung",
        "calculer": "EET Berechnen",
        "correction": "Delta Summe / 10",
        "delta": "Delta",
        "dossard": "Startnummer",
        "dossard_eet": "EET Start-Nr.",
        "eet_calculee": "Berechnete EET",
        "effacer": "Löschen",
        "erreur_aucun_te": "Fehler: keine elektronische Zeit zu berechnen.",
        "erreur_plusieurs_te": "Fehler: mehrere elektronische Zeiten fehlen.",
        "erreur_references": "Fehler: 10 vollständige Referenzzeiten sind erforderlich.",
        "erreur_tm": "Fehler: alle Handzeiten (TOD) müssen eingegeben werden.",
        "exemple_fis": "FIS Beispiel",
        "grille_valide": "Eingabe gültig",
        "langue": "Sprache",
        "pdf": "PDF",
        "nom_pdf": "EET_Berechnung",
        "precision_te": "ET-Genauigkeit",
        "precision_tm": "MT-Genauigkeit",
        "recharger": "Neu laden",
        "references": "Referenzen",
        "resultat": "Ergebnis",
        "resultat_sous_grille": "Ergebnis unter dem Eingabebereich",
        "retour": "Zurück",
        "somme_delta": "Delta Summe",
        "te": "ET (TOD)",
        "temps_electronique": "Elektronische Zeit (TOD)",
        "temps_manuel": "Manuelle Zeit (TOD)",
        "titre": "EET Rechner",
        "tm": "MT (TOD)",
        "meta_description": "EET-Rechner (Equivalent Electronic Time) für alpine Skirennen. Berechnung von Ersatzelektronikzeiten gemäß FIS- und nationalen Zeitmessvorschriften auf Basis von Handzeiten oder Zeitmesssystem B.",
        "calculation_id": "Berechnungs-ID",

        #
        # Berechnungssuche
        #

        "rechercher_calcul": "Berechnung suchen",
        "saison": "Saison",
        "codex": "Codex",
        "rechercher": "Suchen",
        "fermer": "Schließen",
        "discipline": "Disziplin",
        "manche": "Lauf",
        "date": "Datum",
        "lieu": "Ort",
        "consulter": "Anzeigen",
        "aucun_calcul_trouve": "Keine Berechnung gefunden.",

        #
        # Glossar
        #

        "lexique_titre": "Glossar",
        "lexique_precision": "xxxxx",
        "lexique_precision_txt": "Genauigkeit der Zeitmessgeräte.",
        "lexique_tm": "Manuelle Zeit im Tageszeitformat - hh:mm:ss.xxxxxxx",
        "lexique_te": "Elektronische Zeit im Tageszeitformat - hh:mm:ss.xxxxxxx",
        "lexique_eet": "Equivalent Electronic Time im Tageszeitformat - hh:mm:ss.xxxxxxx",
        "lexique_precision_tm": "TM-Genauigkeit",
        "lexique_precision_tm_txt": "Genauigkeit des Zeitmessgeräts für die Eingabe der manuellen Zeiten.",
        "lexique_precision_te": "TE-Genauigkeit",
        "lexique_precision_te_txt": "Genauigkeit des Zeitmessgeräts für die Eingabe der elektronischen Zeiten.",
        "lexique_tod": "TOD = Tageszeit",

        #
        # Aide
        #
      
        "aide": "Hilfe",
        "aide_title": "EET Calculator - Hilfe",
        "aide_calcul": "Berechnung",
        "aide_calcul_l1a": "Auf ",
        "aide_calcul_l1b": "EET berechnen",
        "aide_calcul_l2": "Die Anwendung:",
        "aide_calcul_l3": "berechnet die Differenzen MT − ET der 10 Referenzen;",
        "aide_calcul_l4": "berechnet die durchschnittliche Korrektur;",
        "aide_calcul_l5": "wendet diese Korrektur auf die Handzeit (TOD) des betreffenden Wettkämpfers an;",
        "aide_calcul_l6": "zeigt die berechnete EET an.",
        "aide_calcul_explication_l1": "Ist die Summe der Deltas negativ, sind die manuellen Zeiten (TM) insgesamt kleiner als die elektronischen Zeiten (TE). Die manuellen Ersatzzeiten liegen somit vor den elektronischen Zeiten. Die berechnete Korrektur ist negativ und die resultierende EET ist größer als die manuelle Zeit (TM) des betreffenden Wettkämpfers.",
        "aide_calcul_explication_l2": "Ist die Summe der Deltas hingegen positiv, sind die manuellen Zeiten insgesamt größer als die elektronischen Zeiten. Die manuellen Ersatzzeiten liegen somit hinter den elektronischen Zeiten. Die berechnete Korrektur ist positiv und die resultierende EET ist kleiner als die manuelle Zeit (TM) des betreffenden Wettkämpfers.",
        "aide_exemple_fis": "FIS-Beispiel",
        "aide_exemple_fis_l1a": "Die Schaltfläche ",
        "aide_exemple_fis_l1b": " lädt das in der FIS-Dokumentation verwendete Beispiel, um die Funktionsweise der Anwendung zu überprüfen.",
        "aide_precision_des_temps": "Zeitpräzision",
        "aide_precision_des_temps_l1": "Gemäß den Bestimmungen werden die Berechnungen mit der maximalen Genauigkeit der Zeitmessgeräte durchgeführt.",
        "aide_precision_des_temps_l2": "Aus diesem Grund wandelt die Anwendung die Zeiten in Mikrosekunden um und führt alle Berechnungen mit dieser Genauigkeit durch.",
        "aide_precision_des_temps_l3a": "Die Einstellungen für die ",
        "aide_precision_des_temps_l3b": " und die ",
        "aide_precision_des_temps_l3c": " dienen ausschließlich dazu, die Anzahl der angezeigten und eingegebenen Dezimalstellen festzulegen.",
        "aide_precision_des_temps_l4": "Sie haben keinen Einfluss auf die Genauigkeit der Berechnungen oder auf die berechnete EET.",
        "aide_principe": "Prinzip",
        "aide_principe_l1": "Die Berechnung der EET (Equivalent Electronic Time) ermöglicht die Ermittlung einer äquivalenten elektronischen Zeit (TOD).",
        "aide_principe_l2": "Für die Berechnung werden benötigt:",
        "aide_principe_l3": "11 Wettkämpfer;",
        "aide_principe_l4": "10 Referenz-Wettkämpfer mit Handzeit (TOD) und elektronischer Zeit (TOD);",
        "aide_principe_l5": "1 Wettkämpfer ohne elektronische Zeit.",
        "aide_rapport_pdf": "PDF-Bericht",
        "aide_rapport_pdf_l1a": "Nach der Berechnung erzeugt die Schaltfläche ",
        "aide_rapport_pdf_l1b": " einen Bericht mit:",
        "aide_rapport_pdf_l2": "den eingegebenen Daten;",
        "aide_rapport_pdf_l3": "den Referenzdifferenzen;",
        "aide_rapport_pdf_l4": "der berechneten Korrektur;",
        "aide_rapport_pdf_l5": "der berechneten EET;",
        "aide_rapport_pdf_l6": "Datum und Uhrzeit der Berechnung.",
        "aide_saisie_des_donnees": "Dateneingabe",
        "aide_saisie_des_donnees_l1": "Die 11 Startnummern eingeben.",
        "aide_saisie_des_donnees_l2": "Die Handzeiten (MT - TOD) der 11 Wettkämpfer eingeben. Wenn ein Zeitmesssystem B verfügbar ist, sollten vorzugsweise die Daten des Systems B anstelle der Handzeiten verwendet werden.",
        "aide_saisie_des_donnees_l3": "Die elektronischen Zeiten (ET - TOD) der 10 Referenz-Wettkämpfer eingeben.",
        "aide_saisie_des_donnees_l4": "Die elektronische Zeit des zu berechnenden Wettkämpfers leer lassen.",
        "aide_saisie_des_donnees_l5a": "Prüfen, ob die Meldung",
        "aide_saisie_des_donnees_l5b": "angezeigt wird.",
        "aide_selection_des_references": "Auswahl der Referenzen",
        "aide_selection_des_references_l1": "Für die EET-Berechnung werden immer 10 Referenz-Wettkämpfer verwendet.",
        "aide_selection_des_references_l2": "Die Referenzen werden vorrangig aus den Wettkämpfern ausgewählt, die vor dem Wettkämpfer liegen, für den die elektronische Zeit (TOD) berechnet werden soll.",
        "aide_selection_des_references_l3": "Wenn weniger als 10 Wettkämpfer vor diesem Wettkämpfer liegen, werden die nachfolgenden Wettkämpfer verwendet, um insgesamt 10 Referenzen zu erhalten.",
        "aide_selection_des_references_l4": "Der Wettkämpfer, für den die EET berechnet wird, wird niemals als Referenz verwendet.",

        #
        # Session
        #

        "session_confidentialite": "Die Berechnungen werden ausschließlich im Browser und auf dem verwendeten Gerät gespeichert. Es erfolgt keine Speicherung in einer dauerhaften Datenbank.",
        "session_duree": "Diese Informationen werden nach der letzten Nutzung der Anwendung 8 Stunden lang in der Browsersitzung gespeichert.",
        "session_fin": "Nach Ablauf dieser Frist oder nach dem Löschen der Browserdaten werden die gespeicherten Berechnungen automatisch entfernt.",
        "session_intro": "Der Rechner speichert automatisch:",
        "session_ligne_1": "die letzte Berechnung;",
        "session_ligne_2": "die vorherige Berechnung.",
        "session_titre": "Benutzersitzung",

        #
        # Confidentialité
        #

        "confidentialite_titre": "Datenschutz",
        "confidentialite_intro": "Die Anwendung EET Calculator erhebt keine personenbezogenen Daten.",
        "confidentialite_compte": "Es ist kein Benutzerkonto erforderlich und keine E-Mail-Adresse wird abgefragt.",
        "confidentialite_session": "Die Berechnungen werden ausschließlich in der Browsersitzung gespeichert, um den letzten und den vorherigen Berechnungsvorgang erneut anzeigen zu können. Diese Informationen werden nach Ablauf der Sitzung automatisch gelöscht.",
        "confidentialite_stockage": "Es wird keine Datenbank verwendet und keine Aufzeichnungen der durchgeführten Berechnungen auf dem Server gespeichert.",
        "confidentialite_ip": "Die Anwendung speichert keine IP-Adressen der Benutzer und führt keine statistische oder werbliche Nachverfolgung durch.",

        #
        # Über
        #

        "a_propos_title": "EET Calculator - Über",
        "a_propos": "Über",
        "a_propos_developpement": "Entwicklung:",
        "a_propos_fonction_l1": "EET Calculator dient zur Berechnung der Equivalent Electronic Time (EET) gemäß den Zeitmessregeln des Internationalen Ski- und Snowboardverbandes (FIS).",
        "a_propos_fonction_l2": "Die Anwendung berechnet eine Equivalent Electronic Time aus manuellen und elektronischen Zeiten gemäß den Zeitmessregeln bei FIS- und nationalen Verbandswettkämpfen.",
        "a_propos_fonction_l3": "Zusätzlich enthält die Anwendung einen Zeitrechner für die täglichen Aufgaben der Zeitmessung (Uhrzeiten, Zeitdauern und Zeitdifferenzen).",
        "a_propos_contact": "Kontakt:",

        #
        # Zeitrechner
        #

        "timecalc_title": "EET Calculator - Zeitrechner",
        "calculatrice_horaire": "Zeitrechner",
        "timecalc_titre": "Zeitrechner",
        "timecalc_depart": "Startzeit",
        "timecalc_arrivee": "Zielzeit",
        "timecalc_temps": "Laufzeit",
        "timecalc_precision_tod": "TOD-Genauigkeit",
        "timecalc_precision_temps": "Zeit-Genauigkeit",
        "timecalc_calculer": "Berechnen",
        "timecalc_effacer": "Löschen",
        "timecalc_calcul_ok": "✓ Berechnung erfolgreich.",
        "timecalc_erreur_deux_valeurs": "Fehler: Bitte genau zwei Werte eingeben.",
        "timecalc_erreur_arrivee": "Fehler: Die Zielzeit muss nach der Startzeit liegen.",
        "timecalc_erreur_negative": "Fehler: Die Berechnung ergibt eine negative Zeit.",
        "timecalc_erreur_tod": "Fehler: Ungültige Tageszeit.",
        "timecalc_erreur_duree": "Fehler: Ungültige Laufzeit.",

        "timecalc_aide_title": "EET Calculator - Hilfe - Zeitrechner",
        "timecalc_aide_titre": "Hilfe - Zeitrechner",
        "timecalc_aide_principe": "Prinzip",
        "timecalc_aide_principe_l1": "Geben Sie genau zwei der drei Werte ein: Startzeit, Zielzeit oder Laufzeit. Der dritte Wert wird automatisch berechnet.",

        "timecalc_aide_saisie": "Eingabe",
        "timecalc_aide_saisie_l1": "Geben Sie genau zwei der drei Werte ein.",
        "timecalc_aide_saisie_l2": "Die Trennzeichen ':' und '.' werden während der Eingabe automatisch eingefügt.",
        "timecalc_aide_saisie_l3": "Tageszeiten werden im Format hh:mm:ss.xxxxxx eingegeben.",
        "timecalc_aide_saisie_l4": "Laufzeiten werden im Format hh:mm:ss.xxx eingegeben.",

        "timecalc_aide_precision": "Genauigkeit",
        "timecalc_aide_precision_l1": "Die Genauigkeit der Start- und Zielzeiten (TOD) kann zwischen 3 und 6 Dezimalstellen gewählt werden.",
        "timecalc_aide_precision_l2": "Die Genauigkeit der Laufzeit kann zwischen 2 und 3 Dezimalstellen gewählt werden.",
        "timecalc_aide_precision_l3": "Alle Berechnungen werden mit Mikrosekundengenauigkeit durchgeführt, unabhängig von der angezeigten Genauigkeit.",

        "timecalc_aide_calcul": "Berechnung",
        "timecalc_aide_calcul_l1": "Der Rechner kann folgende Berechnungen durchführen:",
        "timecalc_aide_calcul_l2": "Startzeit + Zielzeit → Laufzeit",
        "timecalc_aide_calcul_l3": "Startzeit + Laufzeit → Zielzeit",
        "timecalc_aide_calcul_l4": "Zielzeit + Laufzeit → Startzeit",

        "timecalc_aide_remarques": "Hinweise",
        "timecalc_aide_remarques_l1": "Wird die Laufzeit berechnet, wird das Ergebnis auf die gewählte Genauigkeit abgeschnitten und niemals gerundet.",
        "timecalc_aide_remarques_l2": "Start- und Zielzeiten müssen zwischen 00:00:00 und 23:59:59 liegen.",
        "timecalc_aide_remarques_l3": "Minuten und Sekunden müssen kleiner als 60 sein.",
        "timecalc_aide_remarques_l4": "Die eingegebenen Daten werden nach dem Verlassen der Seite nicht gespeichert.",

        "timecalc_aide_exemples": "Beispiele",

        "timecalc_aide_ex1": "Berechnung der Laufzeit",
        "timecalc_aide_ex1_l1": "Startzeit: 10:00:00.000000",
        "timecalc_aide_ex1_l2": "Zielzeit: 10:01:12.345678",
        "timecalc_aide_ex1_l3": "Ergebnis: 00:01:12.34",

        "timecalc_aide_ex2": "Berechnung der Zielzeit",
        "timecalc_aide_ex2_l1": "Startzeit: 10:00:00.000000",
        "timecalc_aide_ex2_l2": "Laufzeit: 00:01:12.34",
        "timecalc_aide_ex2_l3": "Ergebnis: 10:01:12.340000",

        "timecalc_aide_ex3": "Berechnung der Startzeit",
        "timecalc_aide_ex3_l1": "Zielzeit: 10:01:12.340000",
        "timecalc_aide_ex3_l2": "Laufzeit: 00:01:12.34",
        "timecalc_aide_ex3_l3": "Ergebnis: 10:00:00.000000",

        "timecalc_aide_remarque_l1": "Alle Berechnungen werden mit Mikrosekundengenauigkeit durchgeführt.",
        "timecalc_aide_remarque_l2": "Wird die Laufzeit berechnet, wird das Ergebnis auf die gewählte Genauigkeit abgeschnitten und niemals gerundet.",
        "timecalc_aide_remarque_l3": "Start- und Zielzeiten müssen zwischen 00:00:00 und 23:59:59 liegen.",

        "erreurs": {
            "dossard_eet_absent": "Es wurde keine EET-Startnummer ausgewählt.",
            "dossard_eet_inconnu": "Die EET-Startnummer existiert nicht.",
            "temps_manuel_absent": "Die manuelle Zeit fehlt.",
            "temps_electronique_absent": "Die elektronische Zeit fehlt.",
        },

        #
        # Pdf
        #

        "pdf_title": "Berechnung der äquivalenten elektronischen Zeit (EET)",
        "date_calcul": "Berechnungsdatum",
        "calculation_id": "Berechnungs-ID",
        "departure": "Start",
        "arrival": "Ziel",
        "missing_impulse": "Fehlender Impuls",
        "eet_bib": "EET-Startnummer",
        "location": "Ort",

    },

}

def get_langue():

    langue = session.get("langue")

    if langue not in SUPPORTED_LANGUAGES:

        langue_navigateur = (
            request.accept_languages.best
        )

        if langue_navigateur:
            langue_navigateur = langue_navigateur[:2]

        if langue_navigateur in SUPPORTED_LANGUAGES:
            langue = langue_navigateur
        else:
            langue = DEFAULT_LANGUAGE

    return langue
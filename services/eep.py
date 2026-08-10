"""
Gestion des échanges EEP avec les systèmes
de chronométrage.
"""

from services import document_store
from services.document import (
    contient_erreurs,
    effacer_resultat_eet,
    enregistrer_document,
    lire_erreurs,
    nouveau_document,
)


from services.importer_eep import (
    importer_document,
    importer_mt,
)

from services.calculation_id import (
    generer_calculation_id,
)

from services.document_store import (
    charger_document,
    rechercher_documents,
)

from services.eep_validator import (
    EEPValidationError,
    valider_eep_delete,
    valider_eep_initial,
    valider_eep_secondaire,
)

from services.validator import (
    valider_document,
)
from version import APP_VERSION, EEP_VERSION


def recevoir_eep(eep_document):

    if est_requete_delete(eep_document):

        valider_eep_delete(
            eep_document,
        )

        document_store.supprimer_calcul(
            eep_document,
        )

        return {
            "status": "ok",
            "calculation_id":
                eep_document["calculation_id"],
        }

    calculation_id = (
        eep_document["calculation_id"]
        .strip()
    )

    if calculation_id == "":
        return _creer_calcul(
            eep_document
        )

    return _recevoir_secondaire(
        eep_document
    )


def rechercher_calculs(
    season,
    codex,
    bib,
):
    """
    Recherche les calculs EEP terminés
    correspondant à une saison,
    un codex et un dossard EET.

    Retourne une liste de documents.
    """

    return rechercher_documents(
        season,
        codex,
        bib,
    )


def _creer_calcul(
    eep_document,
):
    """
    Crée un nouveau calcul EEP.
    """

    #
    # Validation du protocole EEP
    #

    valider_eep_initial(
        eep_document,
    )

    #
    # Création du document
    #

    document = nouveau_document()

    importer_document(
        document,
        eep_document,
    )

    #
    # Validation métier
    #

    valider_document(
        document,
    )

    #
    # Construction de la réponse
    #

    messages = lire_erreurs(
        document,
    ).copy()

    _ajouter_versions(
        messages,
    )

    response = {
        "status": (
            "warning"
            if contient_erreurs(document)
            else "ok"
        ),
        "messages": messages,
    }

    #
    # Sauvegarde uniquement
    # si le document est valide
    #

    if not contient_erreurs(
        document,
    ):

        calculation_id = (
            generer_calculation_id()
        )

        document["calculation_id"] = (
            calculation_id
        )

        enregistrer_document(
            document
        )

        response["calculation_id"] = (
            calculation_id
        )

    return response


def _recevoir_secondaire(
    eep_document,
):
    """
    Importe les temps du système B
    dans un calcul existant.
    """

    #
    # Validation du JSON reçu
    #

    valider_eep_secondaire(
        eep_document,
    )

    #
    # Récupération de l'identifiant
    # du calcul
    #

    calculation_id = (
        eep_document["calculation_id"]
        .strip()
    )

    #
    # Chargement du document
    #

    document = charger_document(
        calculation_id,
    )

    if document is None:
        raise EEPValidationError(
            "Wrong calculation key."
        )

    #
    # Vérification que le JSON B
    # correspond bien au calcul
    #

    verifier_correspondance_course(
        document,
        eep_document,
    )

    #
    # Import des temps manuels
    #

    #
    # Import des temps manuels
    #

    importer_mt(
        document,
        eep_document,
    )

    #
    # Suppression d'un éventuel résultat EET
    # issu d'un calcul précédent
    #

    effacer_resultat_eet(
        document,
    )

    #
    # Validation du document
    #

    valider_document(
        document,
    )

    #
    # Sauvegarde
    #

    enregistrer_document(
        document,
    )

    #
    # Construction de la réponse
    #

    messages = lire_erreurs(
        document,
    ).copy()

    _ajouter_versions(
        messages,
    )

    return {
        "status": (
            "warning"
            if contient_erreurs(
                document,
            )
            else "ok"
        ),
        "calculation_id": (
            calculation_id
        ),
        "messages": messages,
    }


def verifier_correspondance_course(
    document,
    eep_document,
):
    race = document["race"]
    eep_race = eep_document["race"]

    correspondances = (
        ("season", race["season"], eep_race["season"]),
        ("codex", race["codex"], eep_race["codex"]),
        ("run", race["run"], eep_race["run"]),
        (
            "missing_impulse",
            race["missing_impulse"],
            eep_race["missing_impulse"],
        ),
        (
            "eet_bib",
            race["eet_bib"],
            eep_race["eet_bib"],
        ),
    )

    for nom, attendu, recu in correspondances:
        if attendu != recu:
            raise EEPValidationError(
                f"Wrong calculation key ({nom} mismatch)."
            )


def est_requete_delete(
    eep_document,
):
    return (
        "mode" in eep_document
        and
        eep_document["mode"] == "DELETE"
    )


def _ajouter_versions(
    messages,
):
    """
    Ajoute les versions du protocole
    et de l'implémentation aux
    messages de retour.
    """

    messages.insert(
        0,
        f"EEP protocol version {EEP_VERSION}"
    )

    messages.insert(
        1,
        f"EET Calculator version {APP_VERSION}"
    )
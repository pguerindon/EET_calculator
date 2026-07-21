"""
Gestion des échanges EEP avec les systèmes
de chronométrage.
"""

from services.document import (
    nouveau_document,
)

from services.importer_eep import (
    importer_document,
    importer_mt,
)

from services.calculation_id import (
    generer_calculation_id,
    verifier_calculation_id,
)

from services.document_store import (
    sauver_document,
    charger_document,
    rechercher_documents,
)

from services.eep_validator import (
    EEPValidationError,
    valider_eep_initial,
    valider_eep_secondaire,
)


def recevoir_eep(eep_document):
    """
    Traite un document EEP reçu d'un système de chronométrage.

    Sans calculation_id :
        création d'un nouveau calcul.

    Avec calculation_id :
        import des temps du système B.

    Retourne le calculation_id.
    """

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


def sauver_calcul(
    document,
):
    """
    Sauvegarde un calcul EEP.

    Un document sans calculation_id
    n'est pas stocké.

    Retourne True si le document
    a été sauvegardé.
    """

    calculation_id = document["info"].get(
        "calculation_id"
    )

    if not calculation_id:
        return False

    if not verifier_calculation_id(
        calculation_id
    ):
        return False

    sauver_document(
        document
    )

    return True


def _creer_calcul(
    eep_document,
):
    """
    Crée un nouveau calcul EEP.
    """

    valider_eep_initial(
        eep_document
    )

    document = nouveau_document()

    importer_document(
        document,
        eep_document,
    )

    calculation_id = (
        generer_calculation_id()
    )

    document["info"]["calculation_id"] = (
        calculation_id
    )

    sauver_document(
        document
    )

    return calculation_id


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
        eep_document
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
        calculation_id
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

    importer_mt(
        document,
        eep_document,
    )

    #
    # Sauvegarde
    #

    sauver_document(
        document
    )

    return calculation_id


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
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
    valider_eep_initial,
    valider_eep_secondaire,
)


def recevoir_eep(
    eep_document,
):
    """
    Traite un document EEP reçu
    d'un système de chronométrage.

    Sans calculation_id :
        création d'un nouveau calcul.

    Avec calculation_id :
        import des temps du système B.

    Retourne le calculation_id.
    """

    if (
        isinstance(eep_document, dict)
        and "calculation_id" in eep_document
    ):

        return _recevoir_secondaire(
            eep_document
        )

    return _creer_calcul(
        eep_document
    )


def rappeler_calcul(
    calculation_id,
):
    """
    Rappelle un calcul stocké.

    Retourne None si le calculation_id
    est invalide ou inconnu.
    """

    if not verifier_calculation_id(
        calculation_id
    ):

        return None

    return charger_document(
        calculation_id
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

    valider_eep_secondaire(
        eep_document
    )

    calculation_id = eep_document[
        "calculation_id"
    ]

    if not verifier_calculation_id(
        calculation_id
    ):

        return None

    document = charger_document(
        calculation_id
    )

    if document is None:
        return None

    importer_mt(
        document,
        eep_document,
    )

    sauver_document(
        document
    )

    return calculation_id
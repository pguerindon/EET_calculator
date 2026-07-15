"""
Validation du document métier EET Calculator.
"""

from services import constants

from services.document import (
    ajouter_erreur,
    contient_erreurs,
    vider_erreurs,
)

from pprint import pprint

def valider_document(
    document,
):
    """
    Valide le document.
    """

    vider_erreurs(
        document,
    )

    valider_race(
        document,
    )

    if contient_erreurs(document):
        return

    valider_competitors(
        document,
    )

    if contient_erreurs(document):
        return

    valider_calculation(
        document,
    )


def valider_race(
    document,
):
    """
    Valide les informations de la course.
    """

    verifier_et_precision(
        document,
    )


def valider_competitors(
    document,
):
    """
    Valide les concurrents.
    """

    verifier_nombre_competitors(
        document,
    )

    if contient_erreurs(document):
        return

    verifier_bibs_uniques(
        document,
    )

    if contient_erreurs(document):
        return

    verifier_mt(
        document,
    )

    if contient_erreurs(document):
        return

    verifier_eet(
        document,
    )


def valider_calculation(
    document,
):
    """
    Valide les informations nécessaires
    au calcul.
    """

    pass



def verifier_nombre_competitors(
    document
):
    """
    Vérifie que le document contient exactement
    11 concurrents.
    """

    if len(document["competitors"]) != 11:

        ajouter_erreur(
            document,
            constants.ERROR_INVALID_COMPETITOR_COUNT,
            "The document must contain exactly 11 competitors."
        )


def verifier_bibs_uniques(
    document
):
    """
    Vérifie que tous les dossards sont uniques.
    """

    bibs = set()

    for competitor in document["competitors"]:

        bib = competitor["bib"]

        if bib in bibs:

            ajouter_erreur(
                document,
                constants.ERROR_DUPLICATE_BIB,
                "Duplicate bib."
            )

            return

        bibs.add(
            bib
        )


def verifier_eet(
    document,
):
    """
    Vérifie qu'il existe un et un seul concurrent
    sans temps électronique.

    Ce concurrent devient le concurrent EET.
    """

    eet_index = None

    for index, competitor in enumerate(
        document["competitors"]
    ):

        if competitor["et_us"] is not None:
            continue

        if eet_index is not None:

            ajouter_erreur(
                document,
                constants.ERROR_INVALID_ET_COUNT,
                "There must be exactly one missing electronic time.",
            )

            return

        eet_index = index

    if eet_index is None:

        ajouter_erreur(
            document,
            constants.ERROR_INVALID_ET_COUNT,
            "There must be exactly one missing electronic time.",
        )

        return

    document["result"]["eet_index"] = (
        eet_index
    )


def verifier_et_precision(
    document
):
    """
    Vérifie que la précision ET est valide.
    """

    precision = (
        document["race"]["et_precision"]
    )

    if (
        precision is None
        or
        precision < constants.MIN_ET_PRECISION
        or
        precision > constants.MAX_ET_PRECISION
    ):

        ajouter_erreur(
            document,
            constants.ERROR_INVALID_ET_PRECISION,
            "Invalid electronic time precision."
        )


def verifier_mt(
    document
):
    """
    Vérifie que tous les concurrents
    possèdent un temps manuel.
    """

    for competitor in document["competitors"]:

        if competitor["mt_us"] is None:

            ajouter_erreur(
                document,
                constants.ERROR_INVALID_MT,
                "Each competitor must have a manual time."
            )

            return
        

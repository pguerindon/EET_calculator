"""
Validation du document métier EET Calculator.
"""

from services import constants

from services.document import (
    ajouter_erreur,
    contient_erreurs,
    definir_eet_index,
    effacer_eet,
    marquer_eet,
    vider_erreurs,
    rechercher_references,
)

def valider_document(
    document
):
    """
    Valide le document.
    """

    vider_erreurs(
        document
    )

    valider_race(
        document
    )

    if contient_erreurs(document):
        return

    valider_competitors(
        document
    )

    if contient_erreurs(document):
        return    
    
    valider_calculation(
        document
    )


def valider_race(
    document
):
    """
    Valide les informations de la course.
    """

    verifier_missing_impulse(
        document
    )

    if contient_erreurs(
        document
    ):
        return

    verifier_et_precision(
        document
    )


def valider_competitors(
    document
):
    """
    Valide les concurrents.
    """

    verifier_nombre_competitors(
        document
    )

    if contient_erreurs(document):
        return

    verifier_bibs_uniques(
        document
    )

    if contient_erreurs(document):
        return

    verifier_mt(
        document
    )

    if contient_erreurs(document):
        return

    verifier_eet(
        document
    )

    if contient_erreurs(document):
        return

    rechercher_references(
        document
    )

    verifier_nombre_references(
        document
    )


def valider_calculation(
    document
):
    """
    Valide les informations du calcul.
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
    document
):
    """
    Vérifie qu'il existe exactement un concurrent EET
    et l'identifie.
    """

    effacer_eet(document)

    competitor_eet = None

    for index, competitor in enumerate(
        document["competitors"]
    ):

        if competitor["et_us"] is None:

            if competitor_eet is not None:

                ajouter_erreur(
                    document,
                    constants.ERROR_INVALID_ET_COUNT,
                    "There must be exactly one missing electronic time."
                )

                return

            competitor_eet = competitor

            definir_eet_index(
                document,
                index
            )

    if competitor_eet is None:

        ajouter_erreur(
            document,
            constants.ERROR_INVALID_ET_COUNT,
            "There must be exactly one missing electronic time."
        )

        return

    marquer_eet(
        competitor_eet
    )


def verifier_nombre_references(
    document
):
    """
    Vérifie que le calcul EET dispose
    de 10 concurrents de référence.
    """

    if (
        len(document["calculation"]["reference_indexes"])
        != constants.REFERENCE_COMPETITOR_COUNT
    ):

        ajouter_erreur(
            document,
            constants.ERROR_NOT_ENOUGH_REFERENCES,
            "Unable to calculate EET: exactly 10 reference competitors are required."
        )


def verifier_missing_impulse(
    document
):
    """
    Vérifie que l'impulsion manquante est valide.
    """

    missing_impulse = (
        document["race"]["missing_impulse"]
    )

    if missing_impulse not in (
        constants.IMPULSE_START,
        constants.IMPULSE_FINISH,
    ):

        ajouter_erreur(
            document,
            constants.ERROR_INVALID_MISSING_IMPULSE,
            "Invalid missing impulse."
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
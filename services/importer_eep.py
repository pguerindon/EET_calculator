"""
Import des données EEP dans le Document Model EET Calculator.

Ce module traite les entrées EEP provenant des systèmes
de chronométrage.

Il permet :
- l'import initial d'un document EEP ;
- l'import ultérieur des temps d'un système B.

Il ne réalise aucune validation ni aucun calcul.
"""

from services.temps import (
    tod_to_us,
    precision_tod,
)

from services.constants import (
    RACE_SCHEMA,
    COMPETITOR_SCHEMA,
)


# ----------------------------------------------------------------------
# Import initial
# ----------------------------------------------------------------------

def importer_document(
    document,
    eep_document,
):
    """
    Importe un document EEP initial
    dans le Document Model.
    """

    _importer_race(
        document,
        eep_document["race"],
    )

    _importer_competitors(
        document,
        eep_document["competitors"],
    )

    _determiner_et_precision(
        document,
    )


def _importer_race(
    document,
    race_data,
):
    """
    Importe les informations de la course.
    """

    race = document["race"]

    #
    # Copie de tous les champs
    #

    for field, value in race_data.items():
        if field in race:
            race[field] = value


def _importer_competitors(
    document,
    competitors_data,
):
    """
    Importe les concurrents du système A.
    """

    competitors = document["competitors"]

    for competitor, competitor_data in zip(
        competitors,
        competitors_data,
    ):

        _importer_competitor(
            competitor,
            competitor_data,
        )


def _importer_competitor(
    competitor,
    competitor_data,
):
    """
    Importe un concurrent du système A.
    """

    #
    # Copie de tous les champs
    #

    for field in COMPETITOR_SCHEMA:

        if field in competitor_data:
            competitor[field] = competitor_data[field]

    #
    # Normalisation
    #

    if competitor["et_tod"] == "":
        competitor["et_tod"] = None


def _determiner_et_precision(
    document,
):
    """
    Détermine la précision des temps électroniques
    du système A.
    """

    document["race"]["et_precision"] = None

    for competitor in document["competitors"]:

        et_tod = competitor["et_tod"]

        if et_tod is None:
            continue

        document["race"]["et_precision"] = (
            precision_tod(
                et_tod
            )
        )

        return


# ----------------------------------------------------------------------
# Import du système B
# ----------------------------------------------------------------------

def importer_mt(
    document,
    eep_document,
):
    """
    Importe les temps électroniques du système B.

    Dans le Document Model, ces temps deviennent
    les temps de remplacement mt_tod / mt_us.
    """

    competitors_data = eep_document[
        "competitors"
    ]

    for competitor_data in competitors_data:

        bib = competitor_data["bib"]

        competitor = _chercher_competitor(
            document,
            bib,
        )

        if competitor is None:
            continue

        mt_tod = competitor_data[
            "et_tod"
        ]

        competitor["mt_tod"] = mt_tod

        if mt_tod is not None:

            competitor["mt_us"] = tod_to_us(
                mt_tod
            )

        else:

            competitor["mt_us"] = None

    _determiner_mt_precision(
        document
    )


def _chercher_competitor(
    document,
    bib,
):
    """
    Recherche un concurrent par son dossard.
    """

    for competitor in document["competitors"]:

        if competitor["bib"] == bib:
            return competitor

    return None


def _determiner_mt_precision(
    document,
):
    """
    Détermine la précision des temps
    du système B.
    """

    document["race"]["mt_precision"] = None

    for competitor in document["competitors"]:

        mt_tod = competitor["mt_tod"]

        if mt_tod is None:
            continue

        document["race"]["mt_precision"] = (
            precision_tod(
                mt_tod
            )
        )

        return
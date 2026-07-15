"""
Présentation du Document Model pour le formulaire.

Ce module convertit les données du document
en lignes destinées à l'interface.
"""

from services.temps import us_to_duration


def document_vers_lignes(
    document,
):
    """
    Convertit un document
    en lignes du formulaire.
    """

    return [
        _competitor_vers_ligne(
            competitor,
            document,
            index,
        )
        for index, competitor in enumerate(
            document["competitors"]
        )
    ]


def _competitor_vers_ligne(
    competitor,
    document,
    index,
):
    """
    Convertit un concurrent
    en ligne du formulaire.
    """

    ligne = nouvelle_ligne()

    ligne["dossard"] = competitor["bib"]

    ligne["tm"] = (
        competitor["mt_tod"] or ""
    )

    eet_index = document["result"][
        "eet_index"
    ]

    ligne["eet"] = (
        eet_index == index
    )

    if ligne["eet"]:

        ligne["te"] = (
            competitor["eet_tod"] or ""
        )

    else:

        ligne["te"] = (
            competitor["et_tod"] or ""
        )

    if competitor["delta_us"] is not None:

        ligne["delta"] = us_to_duration(
            competitor["delta_us"],
            document["race"]["et_precision"],
        )

    return ligne


def nouvelle_ligne():
    """
    Retourne une ligne vide du formulaire.
    """

    return {
        "dossard": "",
        "tm": "",
        "te": "",
        "delta": "",
        "eet": False,
    }
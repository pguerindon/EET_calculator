"""
Adaptateur entre le document métier
et l'interface Web.
"""

from services.formulaire import (
    nouvelle_ligne,
)

from services.temps import (
    duration_to_us,
    tod_to_us,
    us_to_tod,
    us_to_duration,
)

def document_vers_lignes(
    document
):
    """
    Convertit un document
    en lignes.
    """

    precision = document["race"]["et_precision"]

    lignes = []

    for competitor in document["competitors"]:

        lignes.append(

            _competitor_vers_ligne(
                competitor,
                precision,
            )
        )

    return lignes


def _competitor_vers_ligne(
    competitor,
    precision,
):
    """
    Convertit un competitor
    en ligne du formulaire.
    """

    ligne = nouvelle_ligne()

    ligne["dossard"] = competitor["bib"]

    if competitor["mt_us"] is not None:

        ligne["tm"] = us_to_duration(
            competitor["mt_us"],
            precision,
        )

    if competitor["et_us"] is not None:

        ligne["te"] = us_to_tod(
            competitor["et_us"],
            precision,
        )

    if competitor["delta_us"] is not None:

        ligne["delta"] = us_to_duration(
            competitor["delta_us"],
            precision,
        )

    ligne["eet"] = competitor["eet"]

    return ligne


def document_vers_lignes(
    document
):
    """
    Convertit un document
    en lignes du formulaire.
    """

    precision = document["race"]["et_precision"]

    lignes = []

    for competitor in document["competitors"]:

        lignes.append(
            _competitor_vers_ligne(
                competitor,
                precision,
            )
        )

    return lignes


def _ligne_vers_competitor(
    ligne,
    competitor,
):
    """
    Met à jour un competitor
    à partir d'une ligne du formulaire.
    """

    competitor["bib"] = ligne["dossard"]

    if ligne["tm"]:

        competitor["mt_us"] = duration_to_us(
            ligne["tm"]
        )

    else:

        competitor["mt_us"] = None

    if ligne["te"]:

        competitor["et_us"] = tod_to_us(
            ligne["te"]
        )

    else:

        competitor["et_us"] = None


def lignes_vers_document(
    document,
    lignes,
):
    """
    Met à jour un document
    à partir des lignes du formulaire.
    """

    precision = document["race"]["et_precision"]

    for index, ligne in enumerate(lignes):

        _ligne_vers_competitor(
            ligne,
            document["competitors"][index],
        )


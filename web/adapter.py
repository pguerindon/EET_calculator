"""
Adaptateur entre le document métier
et l'interface Web.
"""

from services.document import nouveau_competitor
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

    tm = ligne["tm"]

    if tm:

        competitor["mt_us"] = duration_to_us(
            tm
        )

    else:

        competitor["mt_us"] = None

    te = ligne["te"]

    if te:

        competitor["et_us"] = tod_to_us(
            te
        )

    else:

        competitor["et_us"] = None

def lignes_vers_document(
    document,
    lignes,
    et_precision,
    mt_precision,
    eet_bib,
):
    """
    Met à jour un document
    à partir du formulaire.
    """

    #
    # Mise à jour de la course
    #

    document["race"]["et_precision"] = (
        et_precision
    )

    document["race"]["mt_precision"] = (
        mt_precision
    )

    #
    # Mise à jour des paramètres du calcul
    #

    document["calculation"]["eet_bib"] = (
        eet_bib
    )

    #
    # Les résultats seront recalculés
    #

    document["calculation"]["reference_indexes"] = []

    document["calculation"]["sum_delta_us"] = 0

    document["calculation"]["correction_us"] = 0

    #
    # Reconstruction complète des concurrents
    #

    document["competitors"].clear()

    for ligne in lignes:

        competitor = nouveau_competitor()

        _ligne_vers_competitor(
            ligne,
            competitor,
        )

        document["competitors"].append(
            competitor
        )
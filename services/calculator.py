"""
Calcul EET.

Ce module effectue le calcul EET à partir
d'un Document Model validé.

Convention du moteur EET

La liste document["competitors"] est toujours
dans l'ordre réel des départs.

Aucune fonction du moteur ne trie cette liste
ni les index de référence.

Les concurrents précédant le concurrent EET
sont retenus en priorité.

Si leur nombre est insuffisant, la liste est
complétée avec les concurrents suivants afin
d'obtenir le nombre requis de références.

Convention utilisée dans tout le moteur :

- mt_us  : heure du jour (Time Of Day) en microsecondes
- et_us  : heure du jour (Time Of Day) en microsecondes
- eet_us : heure du jour (Time Of Day) en microsecondes

Les seules durées sont :

- delta_us
- sum_delta_us
- correction_us

L'EET calculé est une heure du jour.
"""

from services import constants

from services.temps import (
    arrondir_division_fis,
    tronquer_us,
    us_to_tod,
)


def calculer_document(
    document,
):
    """
    Effectue le calcul EET complet.
    """

    if document["info"]["errors"]:
        return

    _rechercher_references(
        document
    )

    _calculer_deltas(
        document
    )

    _calculer_correction(
        document
    )

    _calculer_eet(
        document
    )


def _rechercher_references(
    document,
):
    """
    Détermine les concurrents de référence
    pour le calcul de la correction EET.

    Les concurrents précédant l'EET sont retenus
    en priorité.

    La liste est complétée par les concurrents
    suivants afin d'obtenir le nombre requis
    de références.
    """

    competitors = document["competitors"]

    eet_index = document["result"][
        "eet_index"
    ]

    reference_indexes = []

    premier_index = max(
        0,
        eet_index
        - constants.REFERENCE_COMPETITOR_COUNT,
    )

    #
    # Concurrents précédant l'EET
    #

    for index in range(
        premier_index,
        eet_index,
    ):

        reference_indexes.append(
            index
        )

    #
    # Complément avec les concurrents
    # suivant l'EET
    #

    for index in range(
        eet_index + 1,
        len(competitors),
    ):

        if len(reference_indexes) == (
            constants.REFERENCE_COMPETITOR_COUNT
        ):
            break

        reference_indexes.append(
            index
        )

    document["result"][
        "reference_indexes"
    ] = reference_indexes


def _calculer_deltas(
    document,
):
    """
    Calcule les deltas des concurrents
    de référence.

    Delta = MT - ET
    """

    competitors = document["competitors"]

    reference_indexes = document["result"][
        "reference_indexes"
    ]

    for index in reference_indexes:

        competitor = competitors[
            index
        ]

        competitor["delta_us"] = (
            competitor["mt_us"]
            - competitor["et_us"]
        )


def _calculer_correction(
    document,
):
    """
    Calcule la somme des deltas
    et la correction EET.
    """

    competitors = document["competitors"]

    reference_indexes = document["result"][
        "reference_indexes"
    ]

    sum_delta_us = sum(
        competitors[index]["delta_us"]
        for index in reference_indexes
    )

    document["result"][
        "sum_delta_us"
    ] = sum_delta_us

    document["result"][
        "correction_us"
    ] = arrondir_division_fis(
        sum_delta_us,
        len(reference_indexes),
        document["race"]["et_precision"],
    )


def _calculer_eet(
    document,
):
    """
    Calcule l'Equivalent Electronic Time.

    EET = MT - correction

    L'EET est une heure du jour.

    Le résultat est tronqué à la précision
    du chronomètre électronique.
    """

    eet_index = document["result"][
        "eet_index"
    ]

    competitor = document["competitors"][
        eet_index
    ]

    eet_us = (
        competitor["mt_us"]
        - document["result"]["correction_us"]
    )

    eet_us = tronquer_us(
        eet_us,
        document["race"]["et_precision"],
    )

    competitor["eet_us"] = eet_us

    competitor["eet_tod"] = us_to_tod(
        eet_us,
        document["race"]["et_precision"],
    )
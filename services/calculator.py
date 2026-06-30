"""
Calcul EET.

Ce module effectue le calcul EET à partir
d'un document métier validé.

Convention du moteur EET

La liste document["competitors"] est toujours
dans l'ordre réel des départs.

Aucune fonction du moteur ne trie cette liste
ni les index de référence.

Toutes les opérations utilisent exclusivement
l'ordre des départs.
"""

from services.document import (
    contient_erreurs,
    definir_correction_us,
    definir_reference_indexes,
    definir_delta_us,
    definir_sum_delta_us,
)

from services import constants
from services.temps import(

    arrondir_division_fis,
    tronquer_us, 

)


def calculer_document(
    document
):
    """
    Effectue le calcul EET complet.
    """

    if contient_erreurs(
        document
    ):
        return

    _rechercher_references(
        document
    )

def _rechercher_references(
    document
):
    """
    Détermine les 10 concurrents de référence
    pour le calcul de la correction EET.

    Les concurrents sont toujours conservés
    dans leur ordre de départ.
    """

    competitors = document["competitors"]

    eet_index = document["calculation"]["eet_index"]

    reference_indexes = []

    premier_index = max(
        0,
        eet_index - 10
    )

    #
    # Concurrents avant l'EET
    #

    for index in range(
        premier_index,
        eet_index
    ):

        reference_indexes.append(
            index
        )

    #
    # Complément après l'EET
    #

    for index in range(
        eet_index + 1,
        len(competitors)
    ):

        if len(reference_indexes) == 10:

            break

        reference_indexes.append(
            index
        )

    definir_reference_indexes(
        document,
        reference_indexes
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

    _finaliser_calcul(
        document
    )


def _calculer_deltas(
    document
):
    """
    Calcule les deltas des concurrents de référence.
    """

    competitors = document["competitors"]

    reference_indexes = (
        document["calculation"]["reference_indexes"]
    )

    for index in reference_indexes:

        competitor = competitors[index]

        delta_us = (
            competitor["et_us"]
            - competitor["mt_us"]
        )

        definir_delta_us(
            competitor,
            delta_us
        )


def _calculer_correction(
    document
):
    """
    Calcule la correction EET.
    """

    competitors = document["competitors"]

    reference_indexes = (
        document["calculation"]["reference_indexes"]
    )

    sum_delta_us = 0

    #
    # Somme des 10 deltas
    #

    for index in reference_indexes:

        sum_delta_us += (
            competitors[index]["delta_us"]
        )

    definir_sum_delta_us(
        document,
        sum_delta_us
    )

    #
    # Moyenne arrondie suivant le règlement FIS
    #

    correction_us = arrondir_division_fis(
        sum_delta_us,
        len(reference_indexes)
    )

    definir_correction_us(
        document,
        correction_us
    )


def _calculer_eet(
    document
):
    """
    Calcule le temps électronique
    du concurrent EET.
    """

    eet_index = (
        document["calculation"]["eet_index"]
    )

    competitor = (
        document["competitors"][eet_index]
    )

    eet_us = (
        competitor["mt_us"]
        + document["calculation"]["correction_us"]
    )

    tronquer_us(
        eet_us,
        document["race"]["et_precision"]
    )

    competitor["et_us"] = eet_us


def _finaliser_calcul(document):

    document["calculation"]["nb_references"] = len(
        document["calculation"]["reference_indexes"]
    )
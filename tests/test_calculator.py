"""
Tests du module calculator.

Le moteur de calcul est vérifié à partir
de l'exemple officiel FIS.
"""

from services.calculator import (
    calculer_document,
)

from services.exemples import (
    charger_exemple_fis,
)

from services.document import (
    nouveau_document,
)

from services.validator import (
    valider_document,
)


def test_calculer_document():
    """
    Vérifie le calcul complet
    sur l'exemple officiel FIS.
    """

    document = nouveau_document()

    charger_exemple_fis(
        document
    )

    valider_document(
        document
    )

    assert not document["info"]["errors"]

    calculer_document(
        document
    )

    result = document["calculation"]

    #
    # Vérification du concurrent EET
    #

    assert (
        result["eet_index"]
        == 7
    )

    #
    # Vérification des références
    #

    assert (
        result["reference_indexes"]
        == [
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            8,
            9,
            10,
        ]
    )

    #
    # Vérification des deltas
    #

    deltas = [
        225_600,
        -173_200,
        5_800,
        -366_400,
        -598_800,
        -42_700,
        51_000,
        -125_100,
        -181_900,
        48_100,
    ]

    for delta_us, index in zip(
        deltas,
        result["reference_indexes"],
    ):

        competitor = document["competitors"][
            index
        ]

        assert (
            competitor["delta_us"]
            == delta_us
        )

    #
    # Vérification de la somme des deltas
    #

    assert (
        result["sum_delta_us"]
        == -1_157_600
    )

    #
    # Vérification de la correction FIS
    #

    assert (
        result["correction_us"]
        == -115_800
    )

    #
    # Vérification de l'EET
    #

    competitor = document["competitors"][7]

    assert (
        competitor["bib"]
        == "8"
    )

    #
    # L'ET original reste manquant
    #

    assert (
        competitor["et_tod"]
        is None
    )

    assert (
        competitor["et_us"]
        is None
    )

    #
    # L'EET calculé est stocké séparément
    #

    assert (
        competitor["eet_tod"]
        == "10:07:51.6972"
    )

    assert (
        competitor["eet_us"]
        == 36_471_697_200
    )


def test_calculator():
    """
    Exécute les tests du calculator.
    """

    test_calculer_document()

    print(
        "Tous les tests de calculator sont OK"
    )


if __name__ == "__main__":

    test_calculator()
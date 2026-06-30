"""
Tests du module calculator.
"""

from tests.jeu_reference import (
    creer_document_reference,
)

from services.calculator import (
    calculer_document,
)


def test_calculer_document():
    """
    Vérifie le calcul complet.
    """

    document = creer_document_reference()

    calculer_document(
        document
    )

    #
    # Vérification des deltas
    #

    deltas = [
        100,
        200,
        300,
        400,
        500,
        600,
        700,
        900,
        1000,
        1100,
    ]

    references = (
        document["calculation"]["reference_indexes"]
    )

    for i, index in enumerate(
        references
    ):

        competitor = (
            document["competitors"][index]
        )

        assert (
            competitor["delta_us"]
            == deltas[i]
        )

    #
    # Vérification de la correction
    #

    assert (
        document["calculation"]["sum_delta_us"]
        == 5800
    )

    assert (
        document["calculation"]["correction_us"]
        == 580
    )

    #
    # Vérification de l'EET
    #

    competitor = (
        document["competitors"][7]
    )

    assert (
        competitor["et_us"]
        == 8_000_580
    )


def test_calculator():

    test_calculer_document()

    print(
        "Tous les tests de calculator sont OK"
    )


if __name__ == "__main__":

    test_calculator()
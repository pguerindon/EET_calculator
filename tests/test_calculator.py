"""
Tests du module calculator.
"""

from tests.jeu_reference import (
    creer_document_reference,
)

from services.calculator import (
    calculer_deltas,
    calculer_correction,
    calculer_eet,
)


def test_calculer_deltas():
    """
    Vérifie le calcul des deltas.
    """

    document = creer_document_reference()

    calculer_deltas(
        document
    )

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


def test_calculer_correction():
    """
    Vérifie le calcul de la correction.
    """

    document = creer_document_reference()

    calculer_deltas(
        document
    )

    calculer_correction(
        document
    )

    assert (
        document["calculation"]["sum_delta_us"]
        == 5800
    )

    assert (
        document["calculation"]["correction_us"]
        == 580
    )


def test_calculer_eet():
    """
    Vérifie le calcul de l'EET.
    """

    document = creer_document_reference()

    calculer_deltas(
        document
    )

    calculer_correction(
        document
    )

    calculer_eet(
        document
    )

    competitor = (
        document["competitors"][7]
    )

    assert (
        competitor["et_us"]
        == 8_000_580
    )


def test_calculator():
    """
    Exécute tous les tests du module calculator.
    """

    test_calculer_deltas()

    test_calculer_correction()

    test_calculer_eet()

    print(
        "Tous les tests de calculator sont OK"
    )


if __name__ == "__main__":

    test_calculator()
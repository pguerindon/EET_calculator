from services.document import (
    nouveau_document,
    nouveau_competitor,
    ajouter_competitor,
    definir_et_precision,
    definir_bib,
    definir_mt_us,
    definir_et_us,
    definir_eet_index,
    definir_reference_indexes,
    definir_missing_impulse,
)

from services import constants


def creer_document_reference():
    """
    Crée un document de référence
    pour les tests unitaires.
    """

    document = nouveau_document()

    definir_et_precision(
        document,
        5
    )

    definir_missing_impulse(
        document,
        constants.IMPULSE_FINISH
    )
    
    mt = [
        1_000_000,
        2_000_000,
        3_000_000,
        4_000_000,
        5_000_000,
        6_000_000,
        7_000_000,
        8_000_000,
        9_000_000,
        10_000_000,
        11_000_000,
    ]

    et = [
        1_000_100,
        2_000_200,
        3_000_300,
        4_000_400,
        5_000_500,
        6_000_600,
        7_000_700,
        None,
        9_000_900,
        10_001_000,
        11_001_100,
    ]

    for index in range(11):

        competitor = nouveau_competitor()

        definir_bib(
            competitor,
            index + 1
        )

        definir_mt_us(
            competitor,
            mt[index]
        )

        definir_et_us(
            competitor,
            et[index]
        )

        ajouter_competitor(
            document,
            competitor
        )

    definir_eet_index(
        document,
        7
    )

    definir_reference_indexes(
        document,
        [0, 1, 2, 3, 4, 5, 6, 8, 9, 10]
    )

    return document
from services.document import (
    nouveau_document,
)

def creer_document_reference():
    """
    Crée un document de référence
    pour les tests unitaires.
    """

    document = nouveau_document()

    document["race"]["et_precision"] = 5

    document["race"]["missing_impulse"] = "FINISH"

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

        competitor = document["competitors"][index]

        competitor["bib"] = str(index + 1)

        competitor["mt_us"] = mt[index]

        competitor["et_us"] = et[index]

    document["calculation"]["eet_index"] = 7

    document["calculation"]["reference_indexes"] = [
        0, 1, 2, 3, 4, 5, 6, 8, 9, 10
    ]

    return document
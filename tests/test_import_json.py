"""
Tests du module importer_json.
"""

from services.importer_json import (
    importer_json,
)

from services.temps import (
    tod_to_us,
)


def test_import_json():
    """
    Vérifie l'import du document FIS.
    """

    document = importer_json(
        "examples/fis.json"
    )

    #
    # Document
    #

    assert document is not None

    #
    # Concurrents
    #

    assert len(
        document["competitors"]
    ) == 11

    #
    # Dossards
    #

    assert (
        document["competitors"][0]["bib"]
        == 1
    )

    assert (
        document["competitors"][10]["bib"]
        == 11
    )

    #
    # Concurrent EET
    #

    assert (
        document["competitors"][7]["et_us"]
        is None
    )

    #
    # Précision ET
    #

    assert (
        document["race"]["et_precision"]
        == 4
    )

    #
    # Conversion ET
    #

    assert (
        document["competitors"][0]["et_us"]
        ==
        tod_to_us(
            "10:00:50.1292"
        )
    )

    print(
        "Tous les tests de import_json sont OK"
    )


if __name__ == "__main__":

    test_import_json()
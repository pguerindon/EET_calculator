from services.document import (
    nouveau_document,
    nouveau_competitor,
    ajouter_competitor,
    definir_et_precision,
)

from tests.jeu_reference import (
    creer_document_reference,
)

from web.adapter import (
    document_vers_lignes,
    lignes_vers_document,
)


def test_document_vers_lignes():
    """
    Vérifie la conversion
    document -> lignes.
    """

    document = creer_document_reference()

    lignes = document_vers_lignes(
        document
    )

    assert len(lignes) == 11

    assert lignes[0]["dossard"] == 1

    assert lignes[7]["te"] == ""


def test_lignes_vers_document():
    """
    Vérifie la conversion
    lignes -> document.
    """

    document1 = creer_document_reference()

    lignes = document_vers_lignes(
        document1
    )

    document2 = nouveau_document()

    definir_et_precision(
        document2,
        document1["race"]["et_precision"],
    )

    for _ in range(11):

        ajouter_competitor(
            document2,
            nouveau_competitor()
        )

    lignes_vers_document(
        document2,
        lignes,
    )

    for index in range(11):

        competitor1 = (
            document1["competitors"][index]
        )

        competitor2 = (
            document2["competitors"][index]
        )

        assert (
            competitor1["bib"]
            ==
            competitor2["bib"]
        )

        assert (
            competitor1["mt_us"]
            ==
            competitor2["mt_us"]
        )

        assert (
            competitor1["et_us"]
            ==
            competitor2["et_us"]
        )


def test_adapter():
    """
    Lance tous les tests
    de adapter.py.
    """

    test_document_vers_lignes()

    test_lignes_vers_document()

    print(
        "Tous les tests de adapter sont OK"
    )


if __name__ == "__main__":

    test_adapter()
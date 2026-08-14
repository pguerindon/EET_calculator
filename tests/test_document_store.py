"""
Tests du stockage des documents.
"""

from services.document_store import (
    rechercher_documents,
    sauver_document,
)

from services.calculation_id import (
    generer_calculation_id,
)

from tests.jeu_reference import (
    creer_document_reference,
)

def test_rechercher_documents():
    """
    Vérifie la recherche d'un calcul
    par saison, codex et dossard EET.
    """

    document = creer_document_reference()

    document["calculation_id"] = (
        generer_calculation_id()
    )

    document["race"]["season"] = "2027"
    document["race"]["codex"] = "0951"

    sauver_document(
        document
    )

    documents = rechercher_documents(
        "2027",
        "0951",
        "8",
    )

    assert len(documents) >= 1

    for document in documents:

        assert (
            document["race"]["season"]
            == "2027"
        )

        assert (
            document["race"]["codex"]
            == "0951"
        )

        eet_index = document[
            "calculation"
        ]["eet_index"]

        competitor = document[
            "competitors"
        ][eet_index]

        assert competitor["bib"] == "8"


def test_recherche_inconnue():
    """
    Vérifie qu'une recherche inconnue
    retourne une liste vide.
    """

    documents = rechercher_documents(
        "9999",
        "9999",
        "999999",
    )

    assert documents == []


def test_document_store():
    """
    Exécute les tests du stockage.
    """

    test_rechercher_documents()

    test_recherche_inconnue()

    print(
        "Tous les tests de document_store "
        "sont OK"
    )


if __name__ == "__main__":

    test_document_store()
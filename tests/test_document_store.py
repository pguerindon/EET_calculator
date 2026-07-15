"""
Tests du stockage des documents.
"""

from services.document_store import (
    rechercher_documents,
)


def test_rechercher_documents():
    """
    Vérifie la recherche d'un calcul
    par saison, codex et dossard EET.
    """

    documents = rechercher_documents(
        "2027",
        "0951",
        "11",
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
            "result"
        ]["eet_index"]

        competitor = document[
            "competitors"
        ][eet_index]

        assert competitor["bib"] == "11"

        assert competitor["eet_us"] is not None


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
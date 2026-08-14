"""
Tests du module validator.
"""

from tests.jeu_reference import (
    creer_document_reference,
)

from services.validator import (
    valider_document,
)

from services.document import (
    contient_erreurs,
)


def test_document_valide():
    """
    Vérifie qu'un document de référence
    est valide.
    """

    document = creer_document_reference()

    valider_document(
        document
    )

    if contient_erreurs(document):

        for erreur in document["info"]["errors"]:

            print(erreur)

    assert not contient_erreurs(
        document
    )


def test_validator():
    """
    Exécute tous les tests du module validator.
    """

    test_document_valide()

    print(
        "Tous les tests de validator sont OK"
    )


if __name__ == "__main__":

    test_validator()
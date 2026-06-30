"""
Tests du workflow métier.
"""

from services.document import (
    nouveau_document,
)

from services.workflow import (
    traiter_document,
)


def test_workflow():
    """
    Vérifie qu'un document valide
    est traité sans erreur.
    """

    document = nouveau_document()

    traiter_document(
        document
    )

    print(
        "Tous les tests de workflow sont OK"
    )


if __name__ == "__main__":

    test_workflow()
"""
Tests du module validator.
"""

from tests.jeu_reference import (
    creer_document_reference,
)

from services.validator import (
    valider_document,
)

from services import constants

from services.document import (
    contient_erreurs,
    nouveau_document,
    nouveau_competitor,
    ajouter_competitor,
    definir_et_precision,
    definir_missing_impulse,
    definir_bib,
    definir_mt_us,
    definir_et_us,
    definir_eet_index,
    definir_reference_indexes,
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
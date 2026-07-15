from services.validator import (
    valider_document,
)

from services.calculator import (
    calculer_document,
)


def traiter_document(
    document
):
    """
    Valide puis calcule un document.
    """

    valider_document(
        document
    )

    if document["info"]["errors"]:
        return
    
    calculer_document(
        document
    )
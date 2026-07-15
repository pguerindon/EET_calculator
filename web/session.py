"""
Gestion des documents de la session Flask.

Ce module est le seul autorisé
à manipuler la session Flask.
"""

from copy import deepcopy

from flask import session

from services.document import (
    nouveau_document,
)


CURRENT_DOCUMENT = "current_document"

PREVIOUS_DOCUMENT = "previous_document"


def obtenir_document_courant():
    """
    Retourne le document courant.

    Si aucun document n'existe,
    un nouveau document est créé.
    """

    document = session.get(
        CURRENT_DOCUMENT
    )

    if document is None:

        document = nouveau_document()

        session[
            CURRENT_DOCUMENT
        ] = deepcopy(
            document
        )

    return deepcopy(
        document
    )


def obtenir_document_precedent():
    """
    Retourne le document précédent.

    None est retourné
    s'il n'existe pas.
    """

    document = session.get(
        PREVIOUS_DOCUMENT
    )

    if document is None:

        return None

    return deepcopy(
        document
    )


def definir_document_courant(
    document,
):
    """
    Définit le document courant.

    Le document précédent
    n'est pas modifié.
    """

    session[
        CURRENT_DOCUMENT
    ] = deepcopy(
        document
    )


def enregistrer_nouveau_calcul(
    document,
):
    """
    Enregistre un nouveau calcul.

    Le document courant devient
    le document précédent.
    """

    courant = session.get(
        CURRENT_DOCUMENT
    )

    if courant is not None:

        session[
            PREVIOUS_DOCUMENT
        ] = deepcopy(
            courant
        )

    session[
        CURRENT_DOCUMENT
    ] = deepcopy(
        document
    )


def echanger_documents():
    """
    Échange les documents
    courant et précédent.
    """

    courant = session.get(
        CURRENT_DOCUMENT
    )

    precedent = session.get(
        PREVIOUS_DOCUMENT
    )

    if precedent is None:

        return

    session[
        CURRENT_DOCUMENT
    ] = deepcopy(
        precedent
    )

    if courant is not None:

        session[
            PREVIOUS_DOCUMENT
        ] = deepcopy(
            courant
        )
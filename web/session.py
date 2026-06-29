"""
Gestion des documents de la session Flask.

Ce module est le seul autorisé
à manipuler la session Flask.
"""

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
        ] = document

    return document


def obtenir_document_precedent():
    """
    Retourne le document précédent.
    """

    return session.get(
        PREVIOUS_DOCUMENT
    )


def remplacer_document(
    document
):
    """
    Remplace le document courant.

    L'ancien document devient
    le document précédent.
    """

    precedent = session.get(
        CURRENT_DOCUMENT
    )

    if precedent is not None:

        session[
            PREVIOUS_DOCUMENT
        ] = precedent

    session[
        CURRENT_DOCUMENT
    ] = document


def creer_nouveau_document():
    """
    Crée un nouveau document.
    """

    document = nouveau_document()

    remplacer_document(
        document
    )

    return document

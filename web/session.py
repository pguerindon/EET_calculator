"""
Gestion des documents de la session Flask.

Ce module est le seul autorisé à manipuler
la session Flask.
"""

from flask import session

from services.document import (
    nouveau_document,
)

DOCUMENT = "document"

PREVIOUS_DOCUMENT = "previous_document"


def obtenir_document():
    """
    Retourne le document courant.

    Si aucun document n'existe,
    un nouveau document est créé.
    """

    document = session.get(DOCUMENT)

    if document is None:

        document = nouveau_document()

        session[DOCUMENT] = document

    return document


def definir_document(
    document
):
    """
    Définit le document courant.
    """

    precedent = session.get(DOCUMENT)

    if precedent is not None:

        session[PREVIOUS_DOCUMENT] = precedent

    session[DOCUMENT] = document


def obtenir_document_precedent():
    """
    Retourne le document précédent.
    """

    return session.get(
        PREVIOUS_DOCUMENT
    )


def nouveau_document_session():
    """
    Crée un nouveau document.
    """

    document = nouveau_document()

    definir_document(
        document
    )

    return document
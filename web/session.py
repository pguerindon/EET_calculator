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



WORK_DOCUMENT = "work_document"
CURRENT_CALCULATION = "current_calculation"
PREVIOUS_CALCULATION = "previous_calculation"
READ_ONLY = "lecture_seule"
LANGUAGE = "langue"

#
# Document de travail
#

def obtenir_document_travail():
    """
    Retourne le document de travail.

    Si aucun document n'existe,
    un nouveau document est créé.
    """

    document = session.get(
        WORK_DOCUMENT
    )

    if document is None:

        document = nouveau_document()

        session[
            WORK_DOCUMENT
        ] = deepcopy(
            document
        )

    return deepcopy(
        document
    )


def definir_document_travail(
    document,
):
    """
    Définit le document
    de travail.
    """

    session[
        WORK_DOCUMENT
    ] = deepcopy(
        document
    )


#
# Calcul courant
#

def obtenir_calcul_courant():
    """
    Retourne le calcul courant.

    None est retourné
    s'il n'existe pas.
    """

    document = session.get(
        CURRENT_CALCULATION
    )

    if document is None:

        return None

    return deepcopy(
        document
    )


def definir_calcul_courant(
    document,
):
    """
    Définit le calcul courant.
    """

    session[
        CURRENT_CALCULATION
    ] = deepcopy(
        document
    )

#
# Calcul précédent
#

def obtenir_calcul_precedent():
    """
    Retourne le calcul précédent.

    None est retourné
    s'il n'existe pas.
    """

    document = session.get(
        PREVIOUS_CALCULATION
    )

    if document is None:

        return None

    return deepcopy(
        document
    )


def definir_calcul_precedent(
    document,
):
    """
    Définit le calcul précédent.
    """

    session[
        PREVIOUS_CALCULATION
    ] = deepcopy(
        document
    )


#
# Historique
#

def enregistrer_nouveau_calcul(
    document,
):
    """
    Enregistre un nouveau calcul.

    Le calcul courant devient
    le calcul précédent.

    Le nouveau calcul devient
    le calcul courant.

    Le document de travail est
    synchronisé.
    """

    courant = session.get(
        CURRENT_CALCULATION
    )

    if courant is not None:

        session[
            PREVIOUS_CALCULATION
        ] = deepcopy(
            courant
        )

    session[
        CURRENT_CALCULATION
    ] = deepcopy(
        document
    )

    session[
        WORK_DOCUMENT
    ] = deepcopy(
        document
    )


def echanger_calculs():
    """
    Échange le calcul courant
    et le calcul précédent.

    Le document de travail est
    synchronisé avec le nouveau
    calcul courant.
    """

    courant = session.get(
        CURRENT_CALCULATION
    )

    precedent = session.get(
        PREVIOUS_CALCULATION
    )

    if precedent is None:

        return

    session[
        CURRENT_CALCULATION
    ] = deepcopy(
        precedent
    )

    if courant is not None:

        session[
            PREVIOUS_CALCULATION
        ] = deepcopy(
            courant
        )

    session[
        WORK_DOCUMENT
    ] = deepcopy(
        precedent
    )


def calcul_precedent_existe():
    """
    Indique si un calcul précédent
    est disponible.
    """

    return (
        session.get(
            PREVIOUS_CALCULATION
        )
        is not None
    )


def obtenir_mode_lecture_seule():
    """
    Retourne le mode lecture seule.
    """
    return session.get(
        READ_ONLY,
        False,
    )


def definir_mode_lecture_seule(
    lecture_seule,
):
    """
    Définit le mode lecture seule.
    """
    session[
        READ_ONLY
    ] = lecture_seule


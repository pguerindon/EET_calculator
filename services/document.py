"""
Document métier EET Calculator.
Toutes les structures manipulées par l'application sont créées ici.
Aucun autre module ne doit créer directement une structure
du Document Model.
"""

from copy import deepcopy
from datetime import datetime

from services import constants
from services.calculation_id import verifier_calculation_id
from services.document_store import charger_document
from version import EEP_VERSION


# ----------------------------------------------------------------------
# Constructeurs
# ----------------------------------------------------------------------

def nouveau_document():
    """
    Retourne un nouveau document EET.
    """

    document = deepcopy(constants.DOCUMENT_MODEL)

    document["info"]["version"] = EEP_VERSION

    document["competitors"] = [
        nouveau_competitor()
        for _ in range(constants.COMPETITOR_COUNT)
    ]

    return document


def nouveau_document_info():
    """
    Retourne les informations générales du document.
    """

    info = deepcopy(constants.INFO_MODEL)
    info["version"] = EEP_VERSION
    return info


def nouvelle_race():
    """
    Retourne une nouvelle structure de course.
    """

    return deepcopy(constants.RACE_MODEL)


def nouveau_competitor():
    """
    Retourne une nouvelle structure de concurrent.
    """

    return deepcopy(constants.COMPETITOR_MODEL)


def nouveau_result():
    """
    Retourne une nouvelle structure de calcul.
    """

    return deepcopy(constants.RESULT_MODEL)      


def nouvelle_erreur():
    """
    Retourne une nouvelle erreur.
    """

    return deepcopy(constants.ERROR_MODEL)

# ----------------------------------------------------------------------
# Manipulation du document
# ----------------------------------------------------------------------

def ajouter_erreur(
    document,
    code,
    field="",
):
    """
    Ajoute une erreur au document.
    """

    erreur = nouvelle_erreur()

    erreur["code"] = code
    erreur["field"] = field

    document["info"]["errors"].append(
        erreur
    )


def vider_erreurs(document):
    """
    Supprime toutes les erreurs du document.
    """

    document["info"]["errors"].clear()


def contient_erreurs(document):
    """
    Indique si le document contient des erreurs.
    """

    return bool(document["info"]["errors"])


# ----------------------------------------------------------------------
# Rappel d'un calcul ancien depuis l'interface
# ----------------------------------------------------------------------

def rappeler_calcul(
    calculation_id,
):
    """
    Rappelle un calcul stocké.

    Retourne None si le calculation_id
    est invalide ou inconnu.
    """

    if not verifier_calculation_id(
        calculation_id
    ):

        return None

    return charger_document(
        calculation_id
    )


def formater_date(
    date_iso,
):
    """
    Convertit une date ISO YYYY-MM-DD
    en JJ/MM/AAAA.
    """

    if not date_iso:
        return ""

    try:
        return datetime.strptime(
            date_iso,
            "%Y-%m-%d",
        ).strftime("%d/%m/%Y")

    except ValueError:
        return date_iso
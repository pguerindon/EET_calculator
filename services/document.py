"""
Document métier EET Calculator.
Toutes les structures manipulées par l'application sont créées ici.
Aucun autre module ne doit créer directement une structure
du Document Model.
"""

from copy import deepcopy
from datetime import datetime

from services import constants
from services.calculation_id import generer_calculation_id, verifier_calculation_id
from services.document_store import (
    trouver_calcul_existant,
    charger_document,
    sauver_document,
    supprimer_document,
)
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
    message="",
    field="",
):
    erreur = nouvelle_erreur()

    erreur["code"] = code
    erreur["message"] = message
    erreur["field"] = field

    document["info"]["errors"].append(erreur)


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


def lire_erreurs(document):
    """
    Retourne la liste des erreurs du document.
    """

    return document["info"]["errors"]

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

    document = charger_document(
        calculation_id
    )

    return document


def enregistrer_document(document):

    if document["race"]["missing_impulse"] == "WEB":
        return

    ancien_calculation_id = (
        trouver_calcul_existant(document)
    )

    if ancien_calculation_id:
        supprimer_document(
            ancien_calculation_id
        )

    sauver_document(
        document
    )

    
def normaliser_document(document):
    """
    Met un document en conformité avec la structure
    attendue.

    Les informations existantes sont conservées.
    Les sections, listes et clés manquantes sont créées.
    """

    modele = nouveau_document()

    _fusionner(document, modele)

    return document


def _fusionner(document, modele):

    for cle, valeur in modele.items():

        if cle not in document:
            document[cle] = deepcopy(valeur)
            continue

        if (
            isinstance(document[cle], dict)
            and isinstance(valeur, dict)
        ):
            _fusionner(
                document[cle],
                valeur
            )

        elif (
            isinstance(document[cle], list)
            and isinstance(valeur, list)
            and len(valeur) == 1
        ):
            for element in document[cle]:
                if isinstance(element, dict):
                    _fusionner(
                        element,
                        valeur[0]
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

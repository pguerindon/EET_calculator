"""
Document métier EET Calculator.
Toutes les structures manipulées par l'application sont créées ici.
Aucun autre module ne doit créer directement une structure
du Document Model.
"""

from services import constants


# ----------------------------------------------------------------------
# Constructeurs
# ----------------------------------------------------------------------

def nouveau_document():
    """
    Retourne un nouveau document EET.
    """

    return {
        "info": nouveau_document_info(),
        "race": nouvelle_race(),
        "competitors": [
            nouveau_competitor()
            for _ in range(11)
        ],
        "result": nouveau_result(),
    }


def nouveau_document_info():
    """
    Retourne les informations générales du document.
    """

    return {
        "version": constants.DOCUMENT_VERSION,
        "status": constants.STATUS_NEW,
        "origin": constants.ORIGIN_MANUAL,
        "language": "",
        "errors": []
    }


def nouvelle_race():
    """
    Retourne une nouvelle structure de course.
    """

    return {
        "season": None,
        "codex": "",
        "location": "",
        "date": "",
        "discipline": "",
        "run": 1,
        "et_precision": None,
        "mt_precision": None,
    }


def nouveau_competitor():
    """
    Retourne une nouvelle structure de concurrent.
    """

    return {
    "bib": "",

    "lastname": "",
    "firstname": "",
    "nation": "",

    "et_tod": None,
    "et_us": None,

    "mt_tod": None,
    "mt_us": None,

    "delta_us": None,

    "eet_tod": None,
    "eet_us": None,
    }


def nouveau_result():
    """
    Retourne une nouvelle structure de calcul.
    """

    return {
    "eet_index": None,
    "reference_indexes": [],
    "sum_delta_us": None,
    "correction_us": None,
    }       


def nouvelle_erreur():
    """
    Retourne une nouvelle erreur.
    """

    return {
        "code": "",
        "field": "",
    }

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


def changer_status(document, status):
    """
    Modifie le statut du document.
    """

    document["info"]["status"] = status
    

def definir_origin(
    document,
    origin
):
    """
    Définit l'origine du document.
    """

    document["info"]["origin"] = origin


def obtenir_origin(
    document
):
    """
    Retourne l'origine du document.
    """

    return document["info"]["origin"]

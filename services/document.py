"""
Document métier EET Calculator.

Toutes les structures manipulées par l'application sont créées ici.

Aucun autre module ne doit créer directement un dictionnaire
représentant un document, une course, un concurrent ou un calcul.
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
        "competitors": [],
        "calculation": nouveau_calcul()
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
        "codex": "",
        "race_name": "",
        "location": "",
        "country": "",
        "date": "",
        "discipline": "",
        "gender": "",
        "run": 1,
        "missing_impulse": "",
        "et_precision": None
    }


def nouveau_competitor():
    """
    Retourne une nouvelle structure de concurrent.
    """

    return {
        "bib": "",
        "code": "",
        "lastname": "",
        "firstname": "",
        "gender": "",
        "nation": "",
        "club": "",
        "mt_us": None,
        "et_us": None,
        "delta_us": None,
        "eet": False
    }


def nouveau_calcul():
    """
    Retourne une nouvelle structure de calcul.
    """

    return {
        "eet_index": None,
        "reference_indexes": [],
        "correction_us": None,
    }


def nouvelle_erreur():
    """
    Retourne une nouvelle structure d'erreur.
    """

    return {
        "code": "",
        "message": "",
        "field": ""
    }


# ----------------------------------------------------------------------
# Manipulation du document
# ----------------------------------------------------------------------

def ajouter_competitor(document, competitor):
    """
    Ajoute un concurrent au document.
    """

    document["competitors"].append(competitor)


def ajouter_erreur(document, code, message, field=""):
    """
    Ajoute une erreur au document.
    """

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


def changer_status(document, status):
    """
    Modifie le statut du document.
    """

    document["info"]["status"] = status


def marquer_eet(competitor):
    """
    Marque un concurrent comme étant le concurrent EET.
    """

    competitor["eet"] = True


def effacer_eet(document):
    """
    Supprime l'identification EET
    de tous les concurrents.
    """

    for competitor in document["competitors"]:
        competitor["eet"] = False


def definir_eet_index(
    document,
    index
):
    """
    Définit l'index du concurrent EET.
    """

    document["calculation"]["eet_index"] = index


def definir_reference_indexes(
    document,
    indexes
):
    """
    Définit la liste des concurrents de référence.
    """

    document["calculation"]["reference_indexes"] = indexes


def rechercher_references(
    document
):
    """
    Détermine les 10 concurrents de référence
    pour le calcul de la correction EET.

    Les concurrents sont toujours conservés
    dans leur ordre de départ.
    """

    competitors = document["competitors"]

    eet_index = document["calculation"]["eet_index"]

    reference_indexes = []

    premier_index = max(
        0,
        eet_index - 10
    )

    #
    # Concurrents avant l'EET
    #

    for index in range(
        premier_index,
        eet_index
    ):

        reference_indexes.append(
            index
        )

    #
    # Complément après l'EET
    #

    for index in range(
        eet_index + 1,
        len(competitors)
    ):

        if len(reference_indexes) == 10:

            break

        reference_indexes.append(
            index
        )

    definir_reference_indexes(
        document,
        reference_indexes
    )


def definir_delta_us(
    competitor,
    delta_us
):
    """
    Définit le delta d'un concurrent.
    """

    competitor["delta_us"] = delta_us


def definir_sum_delta_us(
    document,
    sum_delta_us
):
    """
    Définit la somme des deltas.
    """

    document["calculation"]["sum_delta_us"] = (
        sum_delta_us
    )


def definir_correction_us(
    document,
    correction_us
):
    """
    Définit la correction moyenne.
    """

    document["calculation"]["correction_us"] = correction_us


def definir_codex(
    document,
    codex
):
    """
    Définit le codex de la course.
    """

    document["race"]["codex"] = codex


def definir_race_name(
    document,
    race_name
):
    document["race"]["race_name"] = race_name


def definir_location(
    document,
    location
):
    document["race"]["location"] = location


def definir_country(
    document,
    country
):
    document["race"]["country"] = country


def definir_date(
    document,
    date
):
    document["race"]["date"] = date


def definir_discipline(
    document,
    discipline
):
    document["race"]["discipline"] = discipline


def definir_gender(
    document,
    gender
):
    document["race"]["gender"] = gender


def definir_run(
    document,
    run
):
    document["race"]["run"] = run


def definir_missing_impulse(
    document,
    missing_impulse
):
    document["race"]["missing_impulse"] = missing_impulse


def definir_et_precision(
    document,
    precision
):
    document["race"]["et_precision"] = precision


def definir_bib(
    competitor,
    bib
):
    competitor["bib"] = bib


def definir_et_us(
    competitor,
    et_us
):
    """
    Définit le temps électronique.
    """

    competitor["et_us"] = et_us


def definir_mt_us(
    competitor,
    mt_us
):
    """
    Définit le temps manuel.
    """

    competitor["mt_us"] = mt_us


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
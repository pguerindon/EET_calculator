"""
Import des données dans le document métier EET Calculator.

Ce module convertit les données externes
(JSON, formulaire HTML, API...)
vers le document métier interne.
"""

from services.document import (
    nouveau_competitor,
    ajouter_competitor,
    definir_precision,
)

from services.temps import (
    tod_to_us,
    precision_tod,
)


def importer_json(
    document,
    json_data
):
    """
    Importe un document JSON dans le document métier.
    """

    importer_race(
        document,
        json_data.get("race", {})
    )

    importer_competitors(
        document,
        json_data.get("competitors", [])
    )


def importer_race(
    document,
    source
):
    """
    Importe les informations de la course.
    """

    race = document["race"]

    race["codex"] = source.get("codex", "")
    race["name"] = source.get("name", "")
    race["discipline"] = source.get("discipline", "")
    race["gender"] = source.get("gender", "")
    race["run"] = source.get("run", None)
    race["location"] = source.get("location", "")
    race["date"] = source.get("date", "")
    race["missing_impulse"] = source.get(
        "missing_impulse",
        ""
    )


def importer_competitors(
    document,
    competitors
):
    """
    Importe la liste des concurrents.
    """

    for source in competitors:

        competitor = importer_competitor(
            source
        )

        ajouter_competitor(
            document,
            competitor
        )

        et = source.get("et", "")

        if (
            document["calculation"]["precision"] is None
            and et != ""
        ):

            definir_precision(
                document,
                precision_tod(
                    et
                )
            )


def importer_competitor(
    source
):
    """
    Importe un concurrent.
    """

    competitor = nouveau_competitor()

    competitor["bib"] = source.get("bib", "")
    competitor["code"] = source.get("code", "")
    competitor["lastname"] = source.get("lastname", "")
    competitor["firstname"] = source.get("firstname", "")
    competitor["gender"] = source.get("gender", "")
    competitor["nation"] = source.get("nation", "")
    competitor["club"] = source.get("club", "")

    mt = source.get("mt", "")

    if mt != "":

        competitor["mt_us"] = tod_to_us(
            mt
        )

    et = source.get("et", "")

    if et != "":

        competitor["et_us"] = tod_to_us(
            et
        )

    return competitor
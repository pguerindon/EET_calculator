"""
Import d'un document JSON.
"""

import json

from services.document import (
    nouveau_document,
    nouveau_competitor,
    ajouter_competitor,
    definir_codex,
    definir_race_name,
    definir_location,
    definir_country,
    definir_date,
    definir_discipline,
    definir_gender,
    definir_run,
    definir_missing_impulse,
    definir_et_precision,
    definir_bib,
    definir_mt_us,
    definir_et_us,
)

from services.temps import (
    tod_to_us,
    precision_tod,
)


def importer_json(
    filename
):
    """
    Importe un document JSON.
    """

    with open(
        filename,
        encoding="utf-8"
    ) as file:

        json_document = json.load(
            file
        )

    document = nouveau_document()

    importer_race(
        document,
        json_document
    )

    importer_competitors(
        document,
        json_document
    )

    return document


def importer_race(
    document,
    json_document
):
    """
    Importe les informations de la course.
    """

    race = json_document.get(
        "race",
        {}
    )

    definir_codex(
        document,
        race.get("codex", "")
    )

    definir_race_name(
        document,
        race.get("race_name", "")
    )

    definir_location(
        document,
        race.get("location", "")
    )

    definir_country(
        document,
        race.get("country", "")
    )

    definir_date(
        document,
        race.get("date", "")
    )

    definir_discipline(
        document,
        race.get("discipline", "")
    )

    definir_gender(
        document,
        race.get("gender", "")
    )

    definir_run(
        document,
        race.get("run", 1)
    )

    definir_missing_impulse(
        document,
        race.get(
            "missing_impulse",
            ""
        )
    )


def importer_competitors(
    document,
    json_document
):
    """
    Importe les concurrents.
    """

    et_precision = None

    for json_competitor in json_document.get(
        "competitors",
        []
    ):
        competitor = nouveau_competitor()

        definir_bib(
            competitor,
            int(
                json_competitor["bib"]
            )
        )

        definir_mt_us(
            competitor,
            tod_to_us(
                json_competitor["mt"]
            )
        )

        et = json_competitor["et"]

        if et is None:

            definir_et_us(
                competitor,
                None
            )

        else:

            if et_precision is None:

                et_precision = precision_tod(
                    et
                )

            definir_et_us(
                competitor,
                tod_to_us(et)
            )

        ajouter_competitor(
            document,
            competitor
        )

    if et_precision is not None:

        definir_et_precision(
            document,
            et_precision
        )
"""
Import des données du formulaire dans le Document Model.

Ce module reporte les données saisies ou modifiées
dans l'interface vers un document existant.

Il ne réalise aucune validation ni aucun calcul.
"""

from services.temps import tod_to_us


def importer_formulaire(
    document,
    form_data,
):
    """
    Importe les données du formulaire
    dans un document existant.
    """

    _importer_precisions(
        document,
        form_data,
    )

    _importer_competitors(
        document,
        form_data,
    )


def _importer_precisions(
    document,
    form_data,
):
    """
    Importe les précisions des temps.
    """

    mt_precision = form_data.get(
        "precision_tm"
    )

    if mt_precision is not None:
        document["race"]["mt_precision"] = int(
            mt_precision
        )

    et_precision = form_data.get(
        "precision_te"
    )

    if et_precision is not None:
        document["race"]["et_precision"] = int(
            et_precision
        )


def _importer_competitors(
    document,
    form_data,
):
    """
    Importe les données des concurrents.
    """

    for index, competitor in enumerate(
        document["competitors"]
    ):

        _importer_competitor(
            competitor,
            form_data,
            index,
        )


def _importer_competitor(
    competitor,
    form_data,
    index,
):
    """
    Importe une ligne du formulaire
    dans un concurrent existant.
    """

    competitor["bib"] = form_data.get(
        f"dossard_{index}",
        "",
    )

    mt_tod = form_data.get(
        f"tm_{index}",
        "",
    )

    competitor["mt_tod"] = (
        mt_tod or None
    )

    if mt_tod:
        competitor["mt_us"] = tod_to_us(
            mt_tod
        )
    else:
        competitor["mt_us"] = None

    et_tod = form_data.get(
        f"te_{index}",
        "",
    )

    competitor["et_tod"] = (
        et_tod or None
    )

    if et_tod:
        competitor["et_us"] = tod_to_us(
            et_tod
        )
    else:
        competitor["et_us"] = None
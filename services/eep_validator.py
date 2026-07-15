"""
Validation des documents d'échange EEP.

Ce module valide la structure des documents
reçus des systèmes de chronométrage.

Il ne modifie aucune donnée.
"""


class EEPValidationError(Exception):
    """
    Erreur de validation d'un document EEP.
    """

    pass


def valider_eep_initial(
    eep_document,
):
    """
    Valide un document EEP initial
    provenant du système A.
    """

    _valider_document(
        eep_document
    )

    _verifier_champ(
        eep_document,
        "race",
    )

    _valider_race(
        eep_document["race"]
    )

    _valider_competitors(
        eep_document["competitors"]
    )

    nb_et_manquants = sum(
        1
        for competitor
        in eep_document["competitors"]
        if competitor["et_tod"] is None
    )

    if nb_et_manquants != 1:

        raise EEPValidationError(
            "Exactly one ET must be missing."
        )


def valider_eep_secondaire(
    eep_document,
):
    """
    Valide un document EEP provenant
    du système B.

    Les métadonnées race éventuelles
    ne sont pas utilisées.
    """

    _valider_document(
        eep_document
    )

    _verifier_champ(
        eep_document,
        "calculation_id",
    )

    calculation_id = eep_document[
        "calculation_id"
    ]

    if not isinstance(
        calculation_id,
        str,
    ):

        raise EEPValidationError(
            "Invalid calculation_id."
        )

    _valider_competitors(
        eep_document["competitors"]
    )

    nb_et_manquants = sum(
        1
        for competitor
        in eep_document["competitors"]
        if competitor["et_tod"] is None
    )

    if nb_et_manquants != 0:

        raise EEPValidationError(
            "All ET must be present."
        )


def _valider_document(
    eep_document,
):
    """
    Valide la structure générale
    d'un document EEP.
    """

    if not isinstance(
        eep_document,
        dict,
    ):

        raise EEPValidationError(
            "Invalid EEP document."
        )

    _verifier_champ(
        eep_document,
        "competitors",
    )

    if not isinstance(
        eep_document["competitors"],
        list,
    ):

        raise EEPValidationError(
            "Invalid competitors."
        )


def _valider_race(
    race,
):
    """
    Valide les métadonnées de course.
    """

    if not isinstance(
        race,
        dict,
    ):

        raise EEPValidationError(
            "Invalid race."
        )

    champs_obligatoires = (
        "season",
        "codex",
        "location",
        "date",
        "discipline",
        "run",
    )

    for champ in champs_obligatoires:

        _verifier_champ(
            race,
            champ,
        )

    season = race["season"]

    if (
        not isinstance(season, str)
        or len(season) != 4
        or not season.isdigit()
    ):

        raise EEPValidationError(
            "Invalid season."
        )

    codex = race["codex"]

    if (
        not isinstance(codex, str)
        or len(codex) != 4
        or not codex.isdigit()
    ):

        raise EEPValidationError(
            "Invalid codex."
        )


def _valider_competitors(
    competitors,
):
    """
    Valide les concurrents EEP.
    """

    if len(competitors) != 11:

        raise EEPValidationError(
            "The EEP document must contain "
            "exactly 11 competitors."
        )

    for competitor in competitors:

        if not isinstance(
            competitor,
            dict,
        ):

            raise EEPValidationError(
                "Invalid competitor."
            )

        _verifier_champ(
            competitor,
            "bib",
        )

        _verifier_champ(
            competitor,
            "et_tod",
        )


def _verifier_champ(
    data,
    champ,
):
    """
    Vérifie la présence d'un champ obligatoire.
    """

    if champ not in data:

        raise EEPValidationError(
            f"Missing field: {champ}."
        )
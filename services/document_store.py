"""
Stockage des documents EET Calculator.

Chaque document est stocké sous forme JSON
dans le dossier des calculs.

Le calculation_id constitue le nom du fichier.
"""

import json
import os

from config import CALCULS_DIR

def sauver_document(
    document,
):
    """
    Sauvegarde un document.

    Un document existant portant le même
    calculation_id est remplacé.
    """

    calculation_id = document[
        "info"
    ]["calculation_id"]

    CALCULS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    fichier = CALCULS_DIR / (
        f"{calculation_id}.json"
    )

    fichier_temporaire = CALCULS_DIR / (
        f"{calculation_id}.tmp"
    )

    with fichier_temporaire.open(
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            document,
            f,
            ensure_ascii=False,
            indent=2,
        )

    os.replace(
        fichier_temporaire,
        fichier,
    )


def charger_document(
    calculation_id,
):
    """
    Charge un document.

    Retourne None si le document
    n'existe pas.
    """

    fichier = CALCULS_DIR / (
        f"{calculation_id}.json"
    )

    if not fichier.exists():
        return None

    with fichier.open(
        "r",
        encoding="utf-8",
    ) as f:

        return json.load(
            f
        )


def rechercher_documents(
    season,
    codex,
    bib,
):
    """
    Recherche les calculs terminés
    selon les critères renseignés.

    Critères possibles :

    - saison ;
    - codex ;
    - dossard EET.

    Les critères renseignés sont
    combinés par ET.

    Au moins un critère doit être
    renseigné.

    Retourne une liste de documents.
    """

    resultats = []

    season = str(
        season or ""
    ).strip()

    codex = str(
        codex or ""
    ).strip()

    bib = str(
        bib or ""
    ).strip()

    #
    # Une recherche sans critère
    # n'est pas autorisée.
    #

    if not (
        season
        or codex
        or bib
    ):
        return resultats

    if not CALCULS_DIR.exists():
        return resultats

    for fichier in CALCULS_DIR.glob(
        "*.json"
    ):

        document = _charger_fichier(
            fichier
        )

        if document is None:
            continue

        if not _document_calcule(
            document
        ):
            continue

        if not _correspond_recherche(
            document,
            season,
            codex,
            bib,
        ):
            continue

        resultats.append(
            document
        )

    return resultats


def _charger_fichier(
    fichier,
):
    """
    Charge un fichier JSON de calcul.

    Retourne None si le fichier
    ne peut pas être lu.
    """

    try:

        with fichier.open(
            "r",
            encoding="utf-8",
        ) as f:

            return json.load(
                f
            )

    except (
        OSError,
        json.JSONDecodeError,
    ):

        return None


def _document_calcule(
    document,
):
    """
    Indique si le document contient
    un résultat EET calculé.
    """

    try:

        eet_index = document[
            "result"
        ]["eet_index"]

        if eet_index is None:
            return False

        competitor = document[
            "competitors"
        ][eet_index]

        return (
            competitor["eet_us"]
            is not None
        )

    except (
        KeyError,
        IndexError,
        TypeError,
    ):

        return False


def _correspond_recherche(
    document,
    season,
    codex,
    bib,
):
    """
    Indique si le document correspond
    aux critères de recherche renseignés.

    Les critères renseignés sont
    combinés par ET.
    """

    race = document.get(
        "race",
        {}
    )

    result = document.get(
        "result",
        {}
    )

    competitors = document.get(
        "competitors",
        []
    )

    #
    # Saison
    #

    if season:

        document_season = str(
            race.get(
                "season",
                ""
            )
        ).strip()

        if document_season != season:
            return False

    #
    # Codex
    #

    if codex:

        document_codex = str(
            race.get(
                "codex",
                ""
            )
        ).strip()

        if document_codex != codex:
            return False

    #
    # Dossard EET
    #

    if bib:

        eet_index = result.get(
            "eet_index"
        )

        if eet_index is None:
            return False

        try:

            competitor = competitors[
                eet_index
            ]

        except (
            TypeError,
            IndexError,
        ):

            return False

        document_bib = str(
            competitor.get(
                "bib",
                ""
            )
        ).strip()

        if document_bib != bib:
            return False

    return True
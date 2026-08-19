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

    calculation_id = document["calculation_id"]

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

        # trace_document2("dans sauver_document avant json.dump, document = ", document)
        
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


def lister_documents():
    """
    Retourne tous les documents présents
    dans le stockage.

    Les documents invalides ou illisibles
    sont ignorés.
    """

    documents = []

    for fichier in CALCULS_DIR.glob("*.json"):

        document = _charger_fichier(fichier)

        if document is None:
            continue

        documents.append(document)

    return documents


def supprimer_document(
    calculation_id,
):
    """
    Supprime un document.

    Si le document n'existe pas,
    la fonction ne fait rien.
    """

    fichier = CALCULS_DIR / (
        f"{calculation_id}.json"
    )

    if fichier.exists():
        fichier.unlink()


def trouver_calcul_existant(document):

    cle = _cle_metier(document)

    documents = lister_documents()

    for document_existant in documents:

        if _cle_metier(document_existant) == cle:
            return document_existant["calculation_id"]

    return None


def rechercher_documents(
    season,
    codex,
    bib,
):

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

    if not (
        season
        or codex
        or bib
    ):
        return resultats

    for document in lister_documents():

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

    Fonction utilitaire conservée pour
    les traitements de stockage et les
    évolutions futures.
    """

    try:

        eet_index = document[
            "calculation"
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
        "calculation",
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


def _cle_metier(document):

    race = document["race"]

    return (
        race["season"],
        race["codex"],
        race["run"],
        race["eet_bib"],
        race["missing_impulse"],
    )


def verifier_calculs(calculation_ids):

    calculs = {}

    for calculation_id in calculation_ids:

        fichier = CALCULS_DIR / (
            f"{calculation_id}.json"
        )

        document = _charger_fichier(
            fichier
        )

        if document is None:

            calculs[calculation_id] = {
                "exists": False
            }

        else:

            calculs[calculation_id] = {
                "exists": True,
                "mode": document.get(
                    "mode",
                    "",
                ),
            }

    return calculs


def supprimer_document(
    calculation_id,
):
    """
    Supprime un document.
    """

    fichier = (
        CALCULS_DIR
        / f"{calculation_id}.json"
    )

    try:
        fichier.unlink()
    except FileNotFoundError:
        pass


def purger_documents(
    saison,
):
    """
    Supprime tous les documents
    de la saison indiquée.

    Retourne la liste des
    Calculation Keys supprimées.
    """

    calculs_supprimes = []

    documents = lister_documents()

    for document in documents:

        if (
            document["race"]["season"]
            != saison
        ):
            continue

        calculation_id = (
            document["calculation_id"]
        )

        supprimer_document(
            calculation_id,
        )

        calculs_supprimes.append(
            calculation_id
        )

    return calculs_supprimes


def trace_document2(titre, document):

    print()
    print("==========", titre, "==========")

    if document is None:
        print("document : None")
        print("==============================")
        return

    print(f"\n========== {titre} ==========")

    print("calculation_id :", document.get("calculation_id"))
    print("document.calculation :", document["calculation"])

    race = document.get("race", {})
    print("missing_impulse :", race.get("missing_impulse"))
    print("mt_precision    :", race.get("mt_precision"))
    print("et_precision    :", race.get("et_precision"))

    print("id(document) =", id(document))
    print("id(race)     =", id(document["race"]))
    print("id(comp)     =", id(document["competitors"]))
    print("\nConcurrent 8 :")

    c = document["competitors"][7]

    for cle in (
        "bib",
        "name",
        "surname",
        "firstname",
        "lastname",
        "nation",
        "club",
        "mt_tod",
        "et_tod",
        "eet_tod",
    ):
        print(f"  {cle:10} : {c.get(cle)}")

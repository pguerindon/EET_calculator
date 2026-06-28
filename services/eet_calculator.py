from services.temps import (
    delta_tod,
    tod_to_us,
    us_to_tod,
)

from services.eet import (
    calcul_correction_us,
    calcul_eet_us,
    tronquer_us,
)

def compter_temps(
    lignes: list[dict]
) -> tuple[int, int]:
    """
    Compte le nombre de temps manuels et électroniques saisis.
    """

    nb_tm = 0
    nb_te = 0

    for ligne in lignes:

        if (ligne.get("tm") or "").strip():
            nb_tm += 1

        if (ligne.get("te") or "").strip():
            nb_te += 1

    return nb_tm, nb_te


def trouver_ligne_eet(
    lignes: list[dict],
    dossard_eet: str = ""
) -> dict | None:
    """
    Recherche la ligne EET.

    Priorité :
      1. Temps électronique vide.
      2. Dossard fourni (cas PDF).
    """

    for ligne in lignes:

        if ligne["te"] == "":

            ligne["eet"] = True

            return ligne

    if dossard_eet:

        for ligne in lignes:

            if ligne["dossard"] == dossard_eet:

                ligne["eet"] = True

                return ligne

    return None


def extraire_references(
    lignes: list[dict],
    ligne_eet: dict
) -> list[dict]:
    """
    Retourne les lignes servant de références.
    """

    return [
        ligne
        for ligne in lignes
        if ligne is not ligne_eet
    ]


def calculer_deltas(
    references: list[dict],
    precision_delta: int
) -> list[int]:
    """
    Calcule les deltas des références.

    Met à jour le champ 'delta' de chaque référence.

    Retourne la liste des deltas en microsecondes.
    """

    deltas = []

    for ref in references:

        delta = delta_tod(
            ref["tm"],
            ref["te"]
        )

        ref["delta"] = (
            f"{delta / 1_000_000:+.{precision_delta}f}"
        )

        deltas.append(delta)

    return deltas

def calculer_eet(
    ligne_eet: dict,
    deltas: list[int],
    precision_delta: int,
    precision_te: int,
):

    somme_delta_us = sum(deltas)

    somme_delta_txt = (
        f"{somme_delta_us / 1_000_000:+.{precision_delta}f}"
    )

    correction_us = calcul_correction_us(
        deltas,
        precision_te
    )

    correction_txt = (
        f"{correction_us / 1_000_000:+.{precision_te}f}"
    )

    tm_us = tod_to_us(
        ligne_eet["tm"]
    )

    eet_us = calcul_eet_us(
        tm_us,
        correction_us
    )

    eet_us = tronquer_us(
        eet_us,
        precision_te
    )

    eet_txt = us_to_tod(
        eet_us,
        precision_te
    )

    ligne_eet["te"] = eet_txt

    return (
        somme_delta_us,
        somme_delta_txt,
        correction_us,
        correction_txt,
        eet_us,
        eet_txt,
    )

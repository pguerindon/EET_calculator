"""
Préparation et affichage des vues EET Calculator.
"""

from flask import (
    render_template,
    session,
)

from version import APP_VERSION

from translation import (
    TEXTES,
    get_langue,
)

from services.presenter_form import (
    document_vers_lignes,
)

from services.temps import (
    us_to_duration,
)

from web.session import (
    obtenir_calcul_precedent,
    calcul_precedent_existe,
)


def _contexte():
    """
    Retourne le contexte commun à toutes les vues.
    """

    langue = get_langue()

    return langue, TEXTES[langue]


def afficher_calcul(
    document,
    recherche=None,
    resultats_recherche=None,
    recherche_effectuee=False,
):
    """
    Affiche la page principale du calcul EET.
    """

    langue, txt = _contexte()

    lignes = document_vers_lignes(
        document
    )

    race = document["race"]
    result = document["calculation"]

    correction = _formater_duree(
        result["correction_us"],
        race["et_precision"],
    )

    somme_delta = _formater_duree(
        result["sum_delta_us"],
        race["et_precision"],
    )

    eet = ""
    dossard_eet = ""

    eet_index = result["eet_index"]

    if eet_index is not None:

        competitor = document["competitors"][
            eet_index
        ]

        dossard_eet = competitor["bib"]

        eet = competitor["eet_tod"] or ""

    nb_references = len(
        result["reference_indexes"]
    )

    calcul_precedent = (
        _preparer_calcul_precedent()
    )

    if recherche is None:

        recherche = {
            "season": "",
            "codex": "",
            "bib": "",
        }

    if resultats_recherche is None:

        resultats_recherche = []

    lecture_seule = session.get(
        "lecture_seule",
        False,
    )

    return render_template(
        "calcul.html",
        txt=txt,
        langue=langue,
        lignes=lignes,
        correction=correction,
        eet=eet,
        somme_delta=somme_delta,
        precision_te=race["et_precision"],
        precision_tm=race["mt_precision"],
        dossard_eet=dossard_eet,
        nb_references=nb_references,
        calcul_precedent=calcul_precedent,
        calculation_id=(
            ""
            if lecture_seule
            else document[
                "info"
            ].get(
                "calculation_id",
                "",
            )
        ),
        lecture_seule=lecture_seule,
        recherche=recherche,
        resultats_recherche=resultats_recherche,
        recherche_effectuee=(
            recherche_effectuee
        ),
        version=APP_VERSION,
    )


def _formater_duree(
    valeur_us,
    precision,
):
    """
    Formate une durée exprimée en microsecondes.
    """

    if valeur_us is None:
        return ""

    if precision is None:
        return ""

    return us_to_duration(
        valeur_us,
        precision,
    )


def _preparer_calcul_precedent():
    """
    Prépare les informations du calcul précédent.
    """

    if not calcul_precedent_existe():
        return None

    document = obtenir_calcul_precedent()

    result = document["calculation"]

    eet_index = result["eet_index"]

    if eet_index is None:
        return None

    competitor = document["competitors"][
        eet_index
    ]

    if competitor["eet_tod"] is None:
        return None

    return {
        "dossard_eet": competitor["bib"],
        "eet": competitor["eet_tod"],
    }


def _afficher_page(
    template,
    txt,
    langue,
    page_title,
):
    """
    Affiche une page standard.
    """

    return render_template(
        template,
        version=APP_VERSION,
        txt=txt,
        langue=langue,
        page_title=page_title,
    )


def afficher_about():
    """
    Affiche la page À propos.
    """

    langue, txt = _contexte()

    return _afficher_page(
        "about.html",
        txt,
        langue,
        txt["a_propos_title"],
    )


def afficher_help():
    """
    Affiche la page d'aide.
    """

    langue, txt = _contexte()

    return _afficher_page(
        "help.html",
        txt,
        langue,
        txt["aide_title"],
    )


def afficher_timecalc():
    """
    Affiche le calculateur de temps.
    """

    langue, txt = _contexte()

    return _afficher_page(
        "timecalc.html",
        txt,
        langue,
        txt["timecalc_title"],
    )


def afficher_help_timecalc():
    """
    Affiche l'aide du calculateur de temps.
    """

    langue, txt = _contexte()

    return _afficher_page(
        "help_timecalc.html",
        txt,
        langue,
        txt["timecalc_aide_title"],
    )
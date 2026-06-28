from flask import render_template

from config import VERSION


def afficher_calcul(
    txt,
    langue,
    lignes,
    correction="",
    eet="",
    somme_delta="",
    precision_te=4,
    precision_tm=4,
    dossard_eet="",
    nb_references="",
    calcul_precedent=None,
):
    """
    Affiche la page principale du calcul EET.
    """

    return render_template(
        "calcul.html",
        correction=correction,
        txt=txt,
        langue=langue,
        eet=eet,
        somme_delta=somme_delta,
        lignes=lignes,
        precision_te=precision_te,
        precision_tm=precision_tm,
        dossard_eet=dossard_eet,
        calcul_precedent=calcul_precedent,
        nb_references=nb_references,
        version=VERSION,
    )

def afficher_page(
    template,
    txt,
    langue,
    page_title,
):
    return render_template(
        template,
        version=VERSION,
        txt=txt,
        langue=langue,
        page_title=page_title,
    )
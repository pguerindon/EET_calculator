"""
Actions de l'application EET Calculator.
"""

from flask import session

from services.eet_calculator import (
    calculer_deltas,
    calculer_eet,
    trouver_ligne_eet,
    extraire_references,
)

from services.formulaire import (
    initialiser_grille,
    lire_lignes,
)

from services.views import (
    afficher_calcul,
)

from translation import (
    get_langue,
    TEXTES,
)

from flask import (
    redirect,
    session,
)

def changer_langue(
    langue,
):
    """
    Change la langue de l'application.
    """

    session["langue"] = langue

    return redirect("/")

def ouvrir_application(
    txt,
    langue,
    calcul_precedent,
    precision_te_session,
    precision_tm_session,
):
    """
    Gère le premier affichage de l'application.
    """

    dernier_calcul = session.get(
        "dernier_calcul"
    )

    if dernier_calcul:

        return afficher_calcul(
            txt=txt,
            langue=langue,
            lignes=dernier_calcul["lignes"],
            correction=dernier_calcul["correction"],
            eet=dernier_calcul["eet"],
            somme_delta=dernier_calcul["somme_delta"],
            precision_te=dernier_calcul["precision_te"],
            precision_tm=dernier_calcul["precision_tm"],
            dossard_eet=dernier_calcul["dossard_eet"],
            nb_references=dernier_calcul["nb_references"],
            calcul_precedent=calcul_precedent,
        )

    lignes = initialiser_grille()

    return afficher_calcul(
        txt=txt,
        langue=langue,
        lignes=lignes,
        precision_te=precision_te_session,
        precision_tm=precision_tm_session,
        calcul_precedent=calcul_precedent,
    )     


def effectuer_calcul(
    request,
    txt,
    langue,
    calcul_precedent,
):
    """
    Effectue le calcul EET.
    """

    #
    # Calcul du temps électronique équivalent
    #

    precision_te = int(
        request.form.get(
            "precision_te",
            5
        )
    )

    precision_tm = int(
        request.form.get(
            "precision_tm",
            5
        )
    )

    #
    # Un TE ne peut pas être inférieur au millième.
    #

    if precision_te < 3:
        precision_te = 3

    precision_delta = max(
        precision_te,
        precision_tm
    )


    lignes = lire_lignes(request)

    dossard_eet_form = request.form.get(
        "dossard_eet",
        ""
    )
 
    ligne_eet = trouver_ligne_eet(
        lignes,
        dossard_eet_form
    )

    if ligne_eet is None and dossard_eet_form:

        for ligne in lignes:

            if ligne["dossard"] == dossard_eet_form:

                ligne_eet = ligne
                ligne["eet"] = True
                break

    if ligne_eet is None:

        return afficher_calcul(
            txt=txt,
            langue=langue,
            lignes=lignes,
            precision_te=precision_te,
            precision_tm=precision_tm,
            calcul_precedent=calcul_precedent,
        )
    #
    # Constitution des références
    #

    references = extraire_references(
        lignes,
        ligne_eet
    )
    
    try:

        deltas = calculer_deltas(
            references,
            precision_delta
        )

    except ValueError:
        return afficher_calcul(
            txt=txt,
            langue=langue,
            lignes=lignes,
            precision_te=precision_te,
            precision_tm=precision_tm,
            calcul_precedent=calcul_precedent,
        )

    #
    # Calcul de l'EET et mise à jour de la grille
    #

    (
        somme_delta_us,
        somme_delta_txt,
        correction_us,
        correction_txt,
        eet_us,
        eet_txt,
    ) = calculer_eet(
        ligne_eet,
        deltas,
        precision_delta,
        precision_te,
    )

   #
    # Sauvegarde du dernier calcul
    #

    dernier_calcul = {
        "correction": correction_txt,
        "langue": langue,
        "eet": eet_txt,
        "somme_delta": somme_delta_txt,
        "lignes": lignes,
        "precision_te": precision_te,
        "precision_tm": precision_tm,
        "dossard_eet": ligne_eet["dossard"],
        "nb_references": len(references)
    }

    ancien = session.get(
        "dernier_calcul"
    )

    if ancien:
        session["calcul_precedent"] = ancien

    session["dernier_calcul"] = dernier_calcul

    #
    # Affichage du résultat
    #

    return afficher_calcul(
        txt=txt,
        langue=langue,
        lignes=lignes,
        correction=correction_txt,
        eet=eet_txt,
        somme_delta=somme_delta_txt,
        precision_te=precision_te,
        precision_tm=precision_tm,
        dossard_eet=ligne_eet["dossard"],
        calcul_precedent=ancien,
        nb_references=len(references),
    )

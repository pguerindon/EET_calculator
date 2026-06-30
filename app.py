from datetime import timedelta

from flask import (
    Flask,
    jsonify,
    redirect,
    request,
    send_file,
    send_from_directory,
    session,
)

from flask_session import Session

from web.actions import changer_langue, ouvrir_application
from web.adapter import lignes_vers_document
from web.session import (
    obtenir_document_courant,
)

from services.api import (
    charger_references,
)

from config import (
    DEFAULT_LANGUAGE,
    SECRET_KEY, 
)

from pdf import creer_pdf

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
    afficher_page,
)

from translation import (
    get_langue,
    TEXTES,
)

app = Flask(__name__)

app.secret_key = SECRET_KEY

app.config["SESSION_TYPE"] = "filesystem"

app.config["SESSION_PERMANENT"] = True

app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(
    hours=8
)

Session(app)

app.secret_key = SECRET_KEY

@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory(
        "static",
        "sitemap.xml",
        mimetype="application/xml"
    )

@app.route("/robots.txt")
def robots():
    return send_from_directory(
        "static",
        "robots.txt",
        mimetype="text/plain"
    )

@app.route("/google864a4ce7deefd7b4.html")
def google_verification():
    return send_from_directory(
        "static",
        "google864a4ce7deefd7b4.html",
        mimetype="text/html"
    )

@app.route("/about")
def about():

    langue = get_langue()

    txt = TEXTES[langue]

    return afficher_page(
        "about.html",
        txt,
        langue,
        txt["a_propos_title"],
    )

@app.route(
    "/api/load",
    methods=["POST"]
)
def api_load():

    data = request.get_json()

    lignes = charger_references(
        data
    )

    return jsonify(
        {
            "status": "ok",
            "lignes": lignes
        }
    )

@app.route("/help")
def help():

    langue = get_langue()

    txt = TEXTES[langue]

    return afficher_page(
        "help.html",
        txt,
        langue,
        txt["aide_title"],
    )


@app.route("/reload_previous")
def reload_previous():

    precedent = session.get(
        "calcul_precedent"
    )

    courant = session.get(
        "dernier_calcul"
    )

    if precedent:

        session["dernier_calcul"] = precedent

        if courant:
            session["calcul_precedent"] = courant

    return redirect("/")

@app.route("/timecalc")
def timecalc():

    langue = get_langue()

    txt = TEXTES[langue]

    return afficher_page(
        "timecalc.html",
        txt,
        langue,
        txt["timecalc_title"],
    )


@app.route("/help_timecalc")
def help_timecalc():

    langue = get_langue()

    txt = TEXTES[langue]

    return afficher_page(
        "help_timecalc.html",
        txt,
        langue,
        txt["timecalc_aide_title"],
    )

@app.route("/", methods=["GET", "POST"])
def calcul():

    session.permanent = True

    if request.method == "POST":

        action_langue = request.form.get(
            "action_langue"
        )


        langue_form = request.form.get(
            "langue"
        )

        if langue_form:

            session["langue"] = langue_form

        if action_langue == "langue":
            return redirect("/")

        precision_te_form = request.form.get(
            "precision_te"
        )

        if precision_te_form:

            session["precision_te"] = int(
                precision_te_form
            )

        precision_tm_form = request.form.get(
            "precision_tm"
        )

        if precision_tm_form:

            session["precision_tm"] = int(
                precision_tm_form
            )


    langue = get_langue()

    precision_te_session = session.get(
        "precision_te",
        4
    )

    precision_tm_session = session.get(
        "precision_tm",
        4
    )


    txt = TEXTES[langue]

    calcul_precedent = session.get(
        "calcul_precedent"
    )

    #
    # Premier affichage de la page
    #

    if request.method == "GET":

        return ouvrir_application(
            txt,
            langue,
            calcul_precedent,
            precision_te_session,
            precision_tm_session,
        )

    #
    # Récupération de l'action demandée
    #

    action = (
        request.form.get("action_langue")
        or request.form.get("action")
        or "calcul"
    )


    if action == "langue":

        return changer_langue(
            request.form.get(
                "langue",
                DEFAULT_LANGUAGE
            )
        )
    
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

    document = obtenir_document_courant()

    lignes_vers_document(
        document,
        lignes,
    )

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
    # Génération du document PDF
    #

    if action == "pdf":
        
        pdf = creer_pdf(
            lignes,
            ligne_eet["dossard"],
            len(references),
            somme_delta_txt,
            correction_txt,
            eet_txt,
            txt
        )

        return send_file(
            pdf,
            as_attachment=True,
            download_name=f"calcul_eet-{ligne_eet['dossard']}.pdf",
            mimetype="application/pdf"
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


from flask import (
    Flask,
    jsonify,
    request,
    session,
    redirect,
    send_file,
    send_from_directory,
    url_for,
)

from config import DEFAULT_LANGUAGE, SECRET_KEY
from copy import deepcopy

from pdf import creer_pdf

from export_json import (
    exporter_document_json,
)

from services.views import(
    afficher_about,
    afficher_calcul, 
    afficher_help, 
    afficher_help_timecalc, 
    afficher_timecalc,
)

from services.eep import (
    recevoir_eep,
    rechercher_calculs,
    sauver_calcul,
)

from services.document import rappeler_calcul

from services.eep_validator import (
    EEPValidationError,
)

from services.importer_form import (
    importer_formulaire,
)

from services.workflow import traiter_document

from services.exemple_fis import charger_exemple_fis

from web.session import (
    definir_document_travail,
    definir_mode_lecture_seule,
    obtenir_document_travail,
    enregistrer_nouveau_calcul,
    echanger_calculs,
    obtenir_mode_lecture_seule,
)

from services.document import (
    nouveau_document,
)

from translation import (
    get_langue,
    TEXTES,
)

def trace_document(titre, document):

    print(f"\n========== {titre} ==========")

    print("calculation_id :", document.get("calculation_id"))

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


app = Flask(__name__)

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

    return afficher_about()


@app.route("/help")
def help():

    return afficher_help()


@app.route("/timecalc")
def timecalc():

    return afficher_timecalc()


@app.route("/help_timecalc")
def help_timecalc():

    return afficher_help_timecalc()


@app.route(
    "/api/eep",
    methods=["POST"],
)
def api_eep():
    """
    Reçoit un document EEP
    d'un système de chronométrage.
    """

    eep_document = request.get_json(
        silent=True
    )

    try:

        calculation_id = recevoir_eep(
            eep_document
        )

    except EEPValidationError as erreur:

        return jsonify(
            {
                "status": "error",
                "error": str(erreur),
            }
        ), 400

    if calculation_id is None:

        return jsonify(
            {
                "status": "error",
            }
        ), 400

    return jsonify(
        {
            "status": "ok",
            "calculation_id": calculation_id,
        }
    )


@app.route("/reload_previous")
def reload_previous():

    echanger_calculs()

    return redirect("/")


@app.route("/export_json")
def export_json():

    document = obtenir_document_travail()

    exporter_document_json(
        document,
        "document.json",
    )

    return (
        "document.json créé",
        200,
    )


@app.route("/", methods=["GET", "POST"])
def calcul():

    #
    # Lecture de la requête
    #

    action = request.form.get(
        "action"
    )

    consulter_index = request.form.get(
        "consulter_index"
    )

    #
    # Contexte
    #

    langue = get_langue()
    txt = TEXTES[langue]

    #
    # Consultation d'un résultat
    # de recherche publique
    #

    if consulter_index is not None:

        season = (
            request.form.get(
                "search_season",
                "",
            )
            .strip()
        )

        codex = (
            request.form.get(
                "search_codex",
                "",
            )
            .strip()
        )

        bib = (
            request.form.get(
                "search_bib",
                "",
            )
            .strip()
        )

        resultats = rechercher_calculs(
            season,
            codex,
            bib,
        )

        try:

            index = int(
                consulter_index
            )

            document = resultats[index]

        except (
            TypeError,
            ValueError,
            IndexError,
        ):

            return redirect("/")

        definir_mode_lecture_seule(
            True
        )
        definir_document_travail(
            document
        )

        return redirect("/")


    #
    # Changement de langue
    #

    if action == "langue":

        session["langue"] = request.form.get(
            "langue",
            DEFAULT_LANGUAGE,
        )

        return redirect("/")

    #
    # Rappel par Id du calcul
    #
    # La connaissance de l'Id permet
    # de sortir du mode lecture seule.
    #

    if action == "rappeler":

        calculation_id = (
            request.form.get(
                "calculation_id",
                "",
            )
            .strip()
        )

        document = rappeler_calcul(
            calculation_id
        )

        trace_document("document = rappeler_calcul", document)

        if document is not None:

            definir_mode_lecture_seule(
                False
            )
            definir_document_travail(
                document
            )

            # trace_document("après  definir_document_travail", document)


        return redirect("/")

    #
    # Recherche publique
    #

    if action == "rechercher":

        recherche = {
            "season": (
                request.form.get(
                    "search_season",
                    "",
                )
                .strip()
            ),
            "codex": (
                request.form.get(
                    "search_codex",
                    "",
                )
                .strip()
            ),
            "bib": (
                request.form.get(
                    "search_bib",
                    "",
                )
                .strip()
            ),
        }

        resultats_recherche = (
            rechercher_calculs(
                recherche["season"],
                recherche["codex"],
                recherche["bib"],
            )
        )

        document = deepcopy(
            obtenir_document_travail()
        )

        return afficher_calcul(
            document,
            recherche=recherche,
            resultats_recherche=(
                resultats_recherche
            ),
            recherche_effectuee=True,
        )

    #
    # Protection serveur
    # du mode lecture seule
    #

    lecture_seule = (
        obtenir_mode_lecture_seule()
    )

    if (
        request.method == "POST"
        and lecture_seule
        and action in (
            "calcul",
            "effacer",
            "exemple_fis",
        )
    ):

        return redirect("/")

    #
    # Actions créant un nouveau document
    #

    if action == "effacer":

        definir_mode_lecture_seule(
            False
        )

        definir_document_travail(
            nouveau_document()
        )

        return redirect("/")

    if action == "exemple_fis":

        definir_mode_lecture_seule(
            False
        )

        document = nouveau_document()

        charger_exemple_fis(
            document,
        )

        definir_document_travail(
            document
        )

        return redirect("/")

    #
    # Calcul ou affichage
    #

    document = deepcopy(
        obtenir_document_travail()
    )

    if request.method == "POST":


        if action == "calcul":

            # trace_document("dans calcul avant importer_formulaire", document)

            importer_formulaire(
                document,
                request.form,
            )

            # trace_document("dans calcul avant traiter_document", document)

            traiter_document(
                document,
            )

            # trace_document("dans calcul avant sauver_calcul", document)

            sauver_calcul(
                document,
            )

            # trace_document("avant enregistrer_nouveau_calcul", document)

            enregistrer_nouveau_calcul(
                document,
            )

            # trace_document("après enregistrer_nouveau_calcul", document)

            return redirect(
                url_for("calcul")
            )

        elif action == "pdf":

            pdf = creer_pdf(
                document,
                txt,
            )

            eet_bib = document["race"]["eet_bib"]

            nom_fichier = (
                f"EET_{eet_bib}.pdf"
            )

            return send_file(
                pdf,
                as_attachment=True,
                download_name=nom_fichier,
                mimetype="application/pdf",
            )

    #
    # Affichage normal
    #

    return afficher_calcul(
        document
    )

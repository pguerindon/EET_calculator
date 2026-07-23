"""
Génération du rapport PDF EET Calculator.
"""

from io import BytesIO
from datetime import datetime

from flask import request
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet,
)
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from services.calculation_id import calculer_datetime, datetime
from services.constants import COPYRIGHT
from services.document import formater_date
from version import APP_VERSION

from services.temps import (
    us_to_duration,
)

def creer_pdf(document, txt):
    """
    Génère le rapport PDF d'un calcul EET.
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        topMargin=10,
        pagesize=A4,
    )

    #
    # Styles
    #

    styles = getSampleStyleSheet()
    styles_pdf = _creer_styles(styles)

    #
    # Données
    #

    race = document["race"]
    result = document["calculation"]
    competitors = document["competitors"]

    precision_mt = race["mt_precision"]
    precision_et = race["et_precision"]

    eet_index = result["eet_index"]

    competitor_eet = None

    if eet_index is not None:
        competitor_eet = competitors[eet_index]

    document["calculation_id"] = request.form["calculation_id"]

    calculation_id = document["calculation_id"]



    #
    # Logos
    #

    logo_fis = Image(
        "static/images/logo_fis.jpg",
        width=60,
        height=60,
    )

    logo_ffs = Image(
        "static/images/logo_ffs.jpg",
        width=70,
        height=70,
    )

    elements = []

    elements.extend(
        _creer_entete(
            document,
            txt,
            styles_pdf,
            logo_fis,
            logo_ffs,
        )
    )

    elements.append(
        _creer_tableau_competiteurs(
            document,
            txt,
        )
    )

    elements.append(
        Spacer(1, 15)
    )

    elements.append(
        _creer_tableau_resume(
            document,
            txt,
        )
    )

    doc.build(
        elements,
        onFirstPage=lambda canvas, doc: _dessiner_page(canvas, doc, txt),
        onLaterPages=lambda canvas, doc: _dessiner_page(canvas, doc, txt),
    )

    buffer.seek(0)

    return buffer

def _dessiner_page(
    canvas,
    doc,
    txt,
):
    """
    Dessine le pied de page de chaque page.
    """

    canvas.saveState()

    largeur, hauteur = A4

    canvas.setStrokeColor(colors.grey)
    canvas.line(
        doc.leftMargin,
        25,
        largeur - doc.rightMargin,
        25,
    )

    canvas.setFont(
        "Helvetica",
        8,
    )

    canvas.drawString(
        doc.leftMargin,
        12,
        f"{txt['pdf_title']} {APP_VERSION}",
    )

    canvas.drawRightString(
        largeur - doc.rightMargin,
        12,
        COPYRIGHT,
    )

    canvas.restoreState()
    

def _creer_entete(
    document,
    txt,
    styles,
    logo_fis,
    logo_ffs,
):
    """
    Construit l'en-tête du rapport PDF.
    """

    race = document["race"]
    calculation = document["calculation"]
    competitors = document["competitors"]

    #
    # Préparation des données
    #

    competitor_eet = competitors[calculation["eet_index"]]

    dossard = (
        f"{txt['dossard']} "
        f"{competitor_eet['bib']}"
    )

    lastname = competitor_eet["lastname"]
    firstname = competitor_eet["firstname"]

    if race["anonymize_pdf"]:

        lastname = _anonymiser_nom(
            lastname,
            3,
        )

        firstname = _anonymiser_nom(
            firstname,
            1,
        )

    nom = lastname

    if firstname:
        nom += f" {firstname}"

    if competitor_eet["nation"]:
        nom += f" ({competitor_eet['nation']})"

    infos_course = []
    infos_calcul = []

    #
    # Informations de course
    #

    if race["codex"]:
        infos_course.append(
            (
                txt["codex"],
                race["codex"],
            )
        )

    if race["location"]:
        infos_course.append(
            (
                txt["location"],
                race["location"],
            )
        )

    if race["discipline"]:
        infos_course.append(
            (
                txt["discipline"],
                race["discipline"],
            )
        )

    if (
        race["missing_impulse"] != "WEB"
        and race["run"]
    ):
        infos_course.append(
            (
                txt["manche"],
                race["run"],
            )
        )

    if race["date"]:
        infos_course.append(
            (
                txt["date"],
                formater_date(
                    race["date"]
                ),
            )
        )

    #
    # Informations EEP
    #

    if race["missing_impulse"] != "WEB":

        impulsion = {
            "START": txt["departure"],
            "FINISH": txt["arrival"],
        }.get(
            race["missing_impulse"]
        )

        if impulsion:
            infos_calcul.append(
                (
                    txt["missing_impulse"],
                    impulsion,
                )
            )

    #
    # Date du calcul
    #

    if document["calculation_id"]:

        date_calcul = (
            calculer_datetime(
                document["calculation_id"]
            ).strftime(
                "%d/%m/%Y %H:%M:%S"
            )
        )

    else:

        date_calcul = datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        )

    infos_calcul.append(
        (
            txt["date_calcul"],
            date_calcul,
        )
    )

    #
    # Identifiant du calcul
    #

    if document["calculation_id"]:

        infos_calcul.append(
            (
                txt["calculation_id"],
                document["calculation_id"],
            )
        )

    #
    # Titre
    #

    entete = Table(
        [
            [
                logo_fis,
                Paragraph(
                    txt["pdf_title"],
                    styles["titre"],
                ),
                logo_ffs,
            ]
        ],
        colWidths=[90, 320, 90],
    )

    entete.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (0, 0), "LEFT"),
                ("ALIGN", (1, 0), (1, 0), "CENTER"),
                ("ALIGN", (2, 0), (2, 0), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )

    #
    # Construction du document
    #

    elements = []

    elements.append(entete)
    elements.append(Spacer(1, 12))

    _ajouter_paragraphe(
        elements,
        dossard,
        styles["dossard"],
    )

    _ajouter_paragraphe(
        elements,
        nom,
        styles["nom"],
    )

    elements.append(
        Spacer(1, 6)
    )


    #
    # Tableau des informations
    #

    data = []

    for libelle, valeur in infos_course:

        data.append(
            [
                Paragraph(
                    f"{libelle} :",
                    styles["info_libelle"],
                ),
                Paragraph(
                    str(valeur),
                    styles["info_valeur"],
                ),
            ]
        )

    #
    # Séparation entre les informations de course
    # et les informations de calcul.
    #

    if infos_course and infos_calcul:

        data.append(
            [
                Paragraph(
                    "",
                    styles["info_valeur"],
                ),
                Paragraph(
                    "",
                    styles["info_valeur"],
                ),
            ]
        )

    for libelle, valeur in infos_calcul:

        data.append(
            [
                Paragraph(
                    f"{libelle} :",
                    styles["info_libelle"],
                ),
                Paragraph(
                    str(valeur),
                    styles["info_valeur"],
                ),
            ]
        )


    table_infos = Table(
        data,
        colWidths=[145, 215],
    )


    style = [
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0, colors.white),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]

    if infos_course and infos_calcul:

        ligne_separation = len(infos_course)

        style.append(
            (
                "BOTTOMPADDING",
                (0, ligne_separation),
                (-1, ligne_separation),
                8,
            )
        )

    table_infos.setStyle(
        TableStyle(style)
    )


    elements.append(table_infos)
    elements.append(Spacer(1, 18))

    return elements

def _creer_tableau_competiteurs(
    document,
    txt,
):
    """
    Construit le tableau des concurrents.
    """

    race = document["race"]
    result = document["calculation"]
    competitors = document["competitors"]

    precision_et = race["et_precision"]
    eet_index = result["eet_index"]

    #
    # Construction des lignes
    #

    data = [
        [
            txt["dossard"],
            txt["tm"],
            txt["te"],
            txt["delta"],
        ]
    ]

    ligne_eet_pdf = None

    for index, competitor in enumerate(
        competitors,
        start=1,
    ):

        mt = competitor["mt_tod"] or ""
        et = competitor["et_tod"] or ""

        if eet_index == index - 1:

            ligne_eet_pdf = index
            et = competitor["eet_tod"] or ""

        delta = _formater_duree(
            competitor["delta_us"],
            precision_et,
        )

        ligne = [
            competitor["bib"],
            mt,
            et,
            delta,
        ]

        data.append(ligne)

    table = Table(
        data,
        colWidths=[
            55,
            115,
            115,
            80,
        ],
    )


    style = [
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),

        # Fond de l'en-tête
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9D9D9")),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
    ]

    if ligne_eet_pdf is not None:

        style.extend(
            [
                (
                    "BACKGROUND",
                    (0, ligne_eet_pdf),
                    (-1, ligne_eet_pdf),
                    colors.HexColor("#D9D9D9"),
                ),
                (
                    "FONTNAME",
                    (0, ligne_eet_pdf),
                    (-1, ligne_eet_pdf),
                    "Helvetica-Bold",
                ),
            ]
        )

    for index, competitor in enumerate(
        competitors,
        start=1,
    ):

        if competitor["delta_us"] is not None:
            if abs(competitor["delta_us"]) > 1_000_000:

                style.append(
                    (
                        "BACKGROUND",
                        (3, index),
                        (3, index),
                        colors.yellow,
                    )
                )

    table.setStyle(
        TableStyle(style)
    )

    return table


def _creer_tableau_resume(
    document,
    txt,
):
    """
    Construit le tableau récapitulatif du calcul.
    """

    #
    # Préparation des données
    #

    race = document["race"]
    calculation = document["calculation"]

    eet_tod = ""

    if calculation["eet_index"] is not None:
        eet_tod = document["competitors"][
            calculation["eet_index"]
        ]["eet_tod"]

    precision_et = race["et_precision"]

    data = [
        [
            txt["eet_bib"],
            race["eet_bib"],
        ],
        [
            txt["references"],
            len(calculation["reference_indexes"]),
        ],
        [
            txt["somme_delta"],
            _formater_duree(
                calculation["sum_delta_us"],
                precision_et,
            ),
        ],
        [
            txt["correction"],
            _formater_duree(
                calculation["correction_us"],
                precision_et,
            ),
        ],
        [
            txt["eet_calculee"],
            eet_tod,
        ],
    ]

    #
    # Création du tableau
    #

    table = Table(
        data,
        colWidths=[
            180,
            180,
        ],
    )

    #
    # Style
    #

    style = [
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),

        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),

        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),

        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        (
            "BACKGROUND",
            (1, 4),
            (1, 4),
            colors.khaki,
        ),

        (
            "FONTNAME",
            (1, 4),
            (1, 4),
            "Helvetica-Bold",
        ),
    ]

    table.setStyle(
        TableStyle(style)
    )

    return table


def _creer_styles(styles):
    """
    Crée les styles utilisés par le rapport PDF.
    """

    return {

        "titre": ParagraphStyle(
            "Titre",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
            fontSize=17,
            spaceAfter=10,
        ),

        "dossard": ParagraphStyle(
            "Dossard",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
            fontSize=15,
            spaceAfter=4,
        ),

        "nom": ParagraphStyle(
            "Nom",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
            fontSize=15,
            spaceAfter=8,
        ),

        "info": ParagraphStyle(
            "Info",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            fontName="Helvetica",
            fontSize=11,
            spaceAfter=3,
        ),

        "trace": ParagraphStyle(
            "Trace",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            fontName="Helvetica",
            fontSize=10,
            spaceAfter=2,
        ),

        "info_libelle": ParagraphStyle(
            "InfoLibelle",
            parent=styles["Normal"],
            alignment=TA_RIGHT,
            fontName="Helvetica-Bold",
            fontSize=11,
        ),

        "info_valeur": ParagraphStyle(
            "InfoValeur",
            parent=styles["Normal"],
            alignment=TA_LEFT,
            fontName="Helvetica",
            fontSize=11,
        ),
    }


def _ajouter_paragraphe(elements, texte, style):
    """
    Ajoute un paragraphe si le texte n'est pas vide.
    """
    if texte:
        elements.append(Paragraph(texte, style))


def _formater_duree(
    valeur_us,
    precision,
):
    """
    Formate une durée exprimée en microsecondes.
    """

    if valeur_us is None:
        return ""

    return us_to_duration(
        valeur_us,
        precision,
    )


def _anonymiser_nom(
    texte,
    lettres_visibles,
):
    """
    Conserve les premières lettres d'un texte et
    remplace les suivantes par des 'x'.
    """

    if not texte:
        return ""

    if len(texte) <= lettres_visibles:
        return texte

    return (
        texte[:lettres_visibles]
        + "x" * (len(texte) - lettres_visibles)
    )
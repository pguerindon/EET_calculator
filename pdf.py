"""
Génération du rapport PDF EET Calculator.
"""

from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
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

from version import VERSION

from services.temps import (
    us_to_duration,
)


def creer_pdf(
    document,
    txt,
):
    """
    Génère le rapport PDF d'un calcul EET.
    """

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

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        topMargin=10,
    )

    styles = getSampleStyleSheet()

    race = document["race"]
    result = document["result"]
    competitors = document["competitors"]

    precision_mt = race["mt_precision"]
    precision_et = race["et_precision"]

    eet_index = result["eet_index"]

    dossard_eet = ""
    eet = ""

    if eet_index is not None:

        competitor_eet = competitors[
            eet_index
        ]

        dossard_eet = competitor_eet["bib"]

        eet = (
            competitor_eet["eet_tod"]
            or ""
        )

    nb_references = len(
        result["reference_indexes"]
    )

    somme_delta = _formater_duree(
        result["sum_delta_us"],
        precision_et,
    )

    correction = _formater_duree(
        result["correction_us"],
        precision_et,
    )

    entete = Table(
        [
            [
                logo_fis,
                Paragraph(
                    txt["titre"],
                    styles["Title"],
                ),
                logo_ffs,
            ]
        ],
        colWidths=[90, 320, 90],
    )

    entete.setStyle(
        TableStyle(
            [
                (
                    "ALIGN",
                    (0, 0),
                    (0, 0),
                    "LEFT",
                ),
                (
                    "ALIGN",
                    (1, 0),
                    (1, 0),
                    "RIGHT",
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
            ]
        )
    )

    style_version = ParagraphStyle(
        "Version",
        parent=styles["Normal"],
        alignment=1,
        fontName="Helvetica-Bold",
        fontSize=11,
    )

    style_date = ParagraphStyle(
        "Date",
        parent=styles["Normal"],
        alignment=1,
        fontSize=10,
    )

    elements = []

    elements.append(
        entete
    )

    elements.append(
        Paragraph(
            f"Version {VERSION}",
            style_version,
        )
    )

    elements.append(
        Spacer(
            1,
            10,
        )
    )

    elements.append(
        Paragraph(
            f"{txt['date_calcul']} "
            f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            style_date,
        )
    )

    elements.append(
        Spacer(
            1,
            10,
        )
    )

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

        mt = (
            competitor["mt_tod"]
            or ""
        )

        et = (
            competitor["et_tod"]
            or ""
        )

        if (
            eet_index is not None
            and index - 1 == eet_index
        ):

            ligne_eet_pdf = index

            et = (
                competitor["eet_tod"]
                or ""
            )

        delta = _formater_duree(
            competitor["delta_us"],
            precision_et,
        )

        data.append(
            [
                competitor["bib"],
                mt,
                et,
                delta,
            ]
        )

    table = Table(
        data
    )

    if ligne_eet_pdf is not None:

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (2, ligne_eet_pdf),
                        (2, ligne_eet_pdf),
                        colors.khaki,
                    )
                ]
            )
        )

    table.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black,
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER",
                ),
            ]
        )
    )

    elements.append(
        table
    )

    elements.append(
        Spacer(
            1,
            20,
        )
    )

    resume = Table(
        [
            [
                txt["dossard_eet"],
                dossard_eet,
            ],
            [
                txt["references"],
                nb_references,
            ],
            [
                txt["somme_delta"],
                somme_delta,
            ],
            [
                txt["correction"],
                correction,
            ],
            [
                txt["eet_calculee"],
                eet,
            ],
        ],
        colWidths=[137, 137],
    )

    resume.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black,
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.lightgrey,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "ALIGN",
                    (1, 0),
                    (1, -1),
                    "RIGHT",
                ),
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
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, -1),
                    colors.black,
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    11,
                ),
            ]
        )
    )

    elements.append(
        resume
    )

    def metadonnees(
        canvas,
        doc,
    ):
        """
        Définit les métadonnées du PDF.
        """

        canvas.setTitle(
            "Calculateur EET"
        )

        canvas.setAuthor(
            "Philippe Guérindon"
        )

        canvas.setSubject(
            "Equivalent Electronic Time"
        )

    doc.build(
        elements,
        onFirstPage=metadonnees,
    )

    buffer.seek(0)

    return buffer


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
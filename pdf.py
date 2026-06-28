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

from config import VERSION

def creer_pdf(
    lignes,
    dossard_eet,
    nb_references,
    somme_delta,
    correction,
    eet,
    txt
):

    logo_fis = Image(
        "static/images/logo_fis.jpg",
        width=60,
        height=60
    )

    logo_ffs = Image(
        "static/images/logo_ffs.jpg",
        width=70,
        height=70
    )

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        topMargin=10
    )

    styles = getSampleStyleSheet()

    entete = Table(
        [
            [
                logo_fis,
                Paragraph(
                    txt["titre"],
                    styles["Title"]
                ),
                logo_ffs
            ]
        ],
        colWidths=[90, 320, 90]
    )

    entete.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (0, 0), "LEFT"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )

    style_centre = ParagraphStyle(
        "Centre",
        parent=styles["Italic"],
        alignment=1
    )

    style_version = ParagraphStyle(
        "Version",
        parent=styles["Normal"],
        alignment=1,
        fontName="Helvetica-Bold",
        fontSize=11
    )

    style_date = ParagraphStyle(
        "Date",
        parent=styles["Normal"],
        alignment=1,
        fontSize=10
    )

    elements = []

    elements.append(entete)

    elements.append(
        Paragraph(
            f"Version {VERSION}",
            style_version
        )
    )

    elements.append(
        Spacer(1, 10)
    )

    elements.append(
        Paragraph(
            f"{txt['date_calcul']} "
            f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            style_date
        )
    )

    elements.append(
        Spacer(1, 10)
    )

    data = [
        [
            txt["dossard"],
            txt["tm"],
            txt["te"],
            txt["delta"]
        ]
    ]

    ligne_eet_pdf = None

    for index, ligne in enumerate(lignes, start=1):

        if ligne["dossard"] == dossard_eet:
            ligne_eet_pdf = index

        data.append(
            [
                ligne["dossard"],
                ligne["tm"],
                ligne["te"],
                ligne["delta"]
            ]
        )

    table = Table(data)

    if ligne_eet_pdf:

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (2, ligne_eet_pdf),
                        (2, ligne_eet_pdf),
                        colors.khaki
                    )
                ]
            )
        )

    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
        )
    )

    elements.append(table)

    elements.append(
        Spacer(1, 20)
    )

    resume = Table(
        [
            [txt["dossard_eet"], dossard_eet],
            [txt["references"], nb_references],
            [txt["somme_delta"], somme_delta],
            [txt["correction"], correction],
            [txt["eet_calculee"], eet],
        ],
        colWidths=[137, 137]
    )

    resume.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 1, colors.black),

                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),

                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),

                ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),

                # Valeurs alignées à droite
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),

                # EET calculée en jaune
                ("BACKGROUND", (1, 4), (1, 4), colors.khaki),

                # EET en gras
                ("FONTNAME", (1, 4), (1, 4), "Helvetica-Bold"),

                ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                ("FONTSIZE", (0, 0), (-1, -1), 11),               
            ]
        )
    )

    elements.append(
        resume
    )

    def metadonnees(canvas, doc):

        canvas.setTitle("Calculateur EET")
        canvas.setAuthor("Philippe Guérindon")
        canvas.setSubject("Equivalent Electronic Time")

    doc.build(
        elements,
        onFirstPage=metadonnees
    )

    buffer.seek(0)

    return buffer

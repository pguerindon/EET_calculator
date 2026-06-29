"""
Routes Web de EET Calculator.
"""

from flask import render_template

from web.session import (
    obtenir_document_courant,
)


def ouvrir_application():
    """
    Ouvre l'application.

    Crée automatiquement un document
    si aucun document n'existe encore.
    """

    document = obtenir_document_courant()

    #
    # Pour le moment, on ne fait
    # absolument rien du document.
    #

    return render_template(
        "index.html"
    )
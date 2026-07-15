"""
Export d'un document EET au format JSON.
"""

import json


def exporter_document_json(
    document,
    nom_fichier,
):
    """
    Exporte un document
    au format JSON.
    """

    with open(
        nom_fichier,
        "w",
        encoding="utf-8",
    ) as fichier:

        json.dump(
            document,
            fichier,
            indent=4,
            ensure_ascii=False,
        )
"""
Fonctions de traitement des requêtes JSON de l'API REST.
"""

from services.formulaire import initialiser_grille


def charger_references(data):
    """
    Construit la grille de calcul à partir
    d'un document JSON.
    """

    lignes = initialiser_grille()

    references = data.get(
        "references",
        []
    )

    for i, ref in enumerate(references):

        if i >= len(lignes):
            break

        lignes[i]["dossard"] = ref.get(
            "dossard",
            ""
        )

        lignes[i]["te"] = ref.get(
            "te",
            ""
        )

    return lignes
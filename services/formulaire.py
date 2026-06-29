def lire_lignes(request):
    """
    Lit les 11 lignes du formulaire de calcul EET.
    """
    lignes = []

    for i in range(11):

        lignes.append(
            {
                "dossard": request.form.get(
                    f"dossard_{i}"
                ),
                "tm": request.form.get(
                    f"tm_{i}"
                ),
                "te": request.form.get(
                    f"te_{i}"
                ),
                "delta": "",
                "eet": False
            }
        )

    return lignes

def initialiser_grille():
    """
    Retourne une grille vide de 11 lignes.
    """

    return [
        nouvelle_ligne()
        for _ in range(11)
    ]


def nouvelle_ligne():
    """
    Retourne une ligne vide du formulaire.
    """

    return {
        "dossard": "",
        "tm": "",
        "te": "",
        "delta": "",
        "eet": False,
    }
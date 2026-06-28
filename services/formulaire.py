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
    vide les 11 lignes du formulaire de calcul EET.
    """
    lignes = []

    for i in range(11):

        lignes.append(
            {
                "dossard": "",
                "tm": "",
                "te": "",
                "delta": "",
                "eet": False
            }
        )
    return lignes

from translation import TEXTES


LANGUE_REFERENCE = "fr"

LANGUES = (
    "en",
    "de",
)


def comparer_dictionnaires(
    reference,
    traduction,
    chemin="",
):
    """
    Compare récursivement la structure
    de deux dictionnaires de traduction.
    """

    erreurs = []

    cles_reference = set(
        reference.keys()
    )

    cles_traduction = set(
        traduction.keys()
    )

    #
    # Clés manquantes
    #

    for cle in sorted(
        cles_reference - cles_traduction
    ):

        chemin_cle = (
            f"{chemin}.{cle}"
            if chemin
            else cle
        )

        erreurs.append(
            f"Clé manquante : {chemin_cle}"
        )

    #
    # Clés supplémentaires
    #

    for cle in sorted(
        cles_traduction - cles_reference
    ):

        chemin_cle = (
            f"{chemin}.{cle}"
            if chemin
            else cle
        )

        erreurs.append(
            f"Clé supplémentaire : {chemin_cle}"
        )

    #
    # Comparaison récursive
    #

    for cle in sorted(
        cles_reference & cles_traduction
    ):

        valeur_reference = reference[cle]

        valeur_traduction = traduction[cle]

        chemin_cle = (
            f"{chemin}.{cle}"
            if chemin
            else cle
        )

        reference_dict = isinstance(
            valeur_reference,
            dict,
        )

        traduction_dict = isinstance(
            valeur_traduction,
            dict,
        )

        if (
            reference_dict
            and traduction_dict
        ):

            erreurs.extend(
                comparer_dictionnaires(
                    valeur_reference,
                    valeur_traduction,
                    chemin_cle,
                )
            )

        elif (
            reference_dict
            != traduction_dict
        ):

            erreurs.append(
                "Structure différente : "
                f"{chemin_cle}"
            )

    return erreurs


def test_translation():

    reference = TEXTES[
        LANGUE_REFERENCE
    ]

    erreur_trouvee = False

    print()
    print(
        "Langue de référence :",
        LANGUE_REFERENCE,
    )

    print(
        "Nombre de clés :",
        len(reference),
    )

    for langue in LANGUES:

        traduction = TEXTES[langue]

        erreurs = comparer_dictionnaires(
            reference,
            traduction,
        )

        print()
        print(
            f"Vérification {langue}"
        )

        print(
            "Nombre de clés :",
            len(traduction),
        )

        if erreurs:

            erreur_trouvee = True

            for erreur in erreurs:

                print(
                    "ERREUR :",
                    erreur,
                )

        else:

            print(
                "OK - structure identique"
            )

    if erreur_trouvee:

        raise AssertionError(
            "Les traductions sont incohérentes."
        )

    print()
    print(
        "Toutes les traductions sont cohérentes."
    )


if __name__ == "__main__":

    test_translation()
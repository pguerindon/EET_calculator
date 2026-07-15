"""
Tests du flux EEP système A / système B.
"""

from services.eep import (
    recevoir_eep,
    rappeler_calcul,
    rechercher_calculs,
    sauver_calcul,
)

from services.workflow import traiter_document

from services.eep_validator import (
    EEPValidationError,
)

from services.importer_form import (
    importer_formulaire,
)

def creer_eep_a():
    """
    Crée un document EEP simulant
    le système de chronométrage A.
    """

    return {
        "race": {
            "season": "2027",
            "codex": "0951",
            "location": "Chamonix",
            "date": "2026-07-14",
            "discipline": "SL",
            "run": 1,
        },
        "competitors": [
            {
                "bib": str(index + 1),
                "et_tod": (
                    None
                    if index == 10
                    else
                    f"10:00:{index:02d}.12345"
                ),
            }
            for index in range(11)
        ],
    }


def creer_eep_b(
    calculation_id,
):
    """
    Crée un document EEP simulant
    le système de chronométrage B.
    """

    return {
        "calculation_id": calculation_id,
        "race": {
            "season": "2027",
            "codex": "0951",
            "location": "Chamonix",
            "date": "2026-07-14",
            "discipline": "SL",
            "run": 1,
        },
        "competitors": [
            {
                "bib": str(index + 1),
                "et_tod": (
                    f"10:00:{index:02d}.123"
                ),
            }
            for index in range(11)
        ],
    }


def test_flux_eep():
    """
    Vérifie le flux complet EEP.

    Système A :
        création du calcul.

    Système B :
        import des ET comme temps
        de remplacement.

    Rappel :
        récupération du document enrichi.
    """

    #
    # Système A
    #

    eep_a = creer_eep_a()

    calculation_id = recevoir_eep(
        eep_a
    )

    assert calculation_id is not None

    assert len(calculation_id) == 6

    #
    # Rappel après système A
    #

    document = rappeler_calcul(
        calculation_id
    )

    assert document is not None

    assert (
        document["info"]["calculation_id"]
        == calculation_id
    )

    assert (
        document["race"]["season"]
        == "2027"
    )

    assert (
        document["race"]["codex"]
        == "0951"
    )

    assert (
        document["race"]["et_precision"]
        == 5
    )

    assert (
        document["race"]["mt_precision"]
        is None
    )

    assert (
        len(document["competitors"])
        == 11
    )

    #
    # Vérification de l'ET manquant
    #

    competitor = document["competitors"][10]

    assert competitor["bib"] == "11"

    assert competitor["et_tod"] is None

    assert competitor["et_us"] is None

    #
    # Système B
    #

    eep_b = creer_eep_b(
        calculation_id
    )

    resultat = recevoir_eep(
        eep_b
    )

    assert (
        resultat
        == calculation_id
    )

    #
    # Rappel du document enrichi
    #

    document = rappeler_calcul(
        calculation_id
    )

    assert document is not None

    assert (
        document["race"]["season"]
        == "2027"
    )

    assert (
        document["race"]["codex"]
        == "0951"
    )

    assert (
        document["race"]["et_precision"]
        == 5
    )

    assert (
        document["race"]["mt_precision"]
        == 3
    )

    #
    # Vérification des concurrents
    #

    for index, competitor in enumerate(
        document["competitors"]
    ):

        assert (
            competitor["bib"]
            == str(index + 1)
        )

        assert (
            competitor["mt_tod"]
            == f"10:00:{index:02d}.123"
        )

        assert (
            competitor["mt_us"]
            is not None
        )

        if index == 10:

            assert competitor["et_tod"] is None

            assert competitor["et_us"] is None

        else:

            assert (
                competitor["et_tod"]
                == f"10:00:{index:02d}.12345"
            )

            assert (
                competitor["et_us"]
                is not None
            )


def test_systeme_b_sans_calculation_id():
    """
    Vérifie qu'un document du système B
    sans calculation_id est interprété
    comme une demande de nouveau calcul.

    Les 11 ET étant présents,
    le document doit être refusé.
    """

    eep_b = creer_eep_b(
        "000000"
    )

    del eep_b["calculation_id"]

    try:

        recevoir_eep(
            eep_b
        )

    except EEPValidationError as erreur:

        assert (
            str(erreur)
            == "Exactly one ET must be missing."
        )

    else:

        assert False


def test_calculation_id_invalide():
    """
    Vérifie qu'un calculation_id invalide
    ne permet pas de rappeler un document.
    """

    document = rappeler_calcul(
        "ABC"
    )

    assert document is None


def test_rechercher_calculs():
    """
    Vérifie la recherche publique
    des calculs EEP par métadonnées.
    """

    #
    # Création d'un calcul terminé
    #

    eep_a = {
        "race": {
            "season": "2027",
            "codex": "0951",
            "location": "Chamonix",
            "date": "2026-07-14",
            "discipline": "SL",
            "run": 1,
        },
        "competitors": [],
    }

    #
    # 10 ET de référence
    #

    for index in range(10):

        eep_a["competitors"].append(
            {
                "bib": str(
                    index + 1
                ),
                "et_tod": (
                    "10:00:"
                    f"{index:02d}.12345"
                ),
            }
        )

    #
    # ET manquant
    #

    eep_a["competitors"].append(
        {
            "bib": "11",
            "et_tod": None,
        }
    )

    #
    # Création du calcul
    #

    calculation_id = recevoir_eep(
        eep_a
    )

    document = rappeler_calcul(
        calculation_id
    )

    assert document is not None

    #
    # Saisie des MT
    #

    formulaire = {
        "precision_tm": "3",
        "dossard_eet": "11",
    }

    for index in range(11):

        formulaire[
            f"dossard_{index}"
        ] = str(
            index + 1
        )

        formulaire[
            f"tm_{index}"
        ] = (
            "10:00:"
            f"{index:02d}.223"
        )

        formulaire[
            f"te_{index}"
        ] = (
            ""
            if index == 10
            else (
                "10:00:"
                f"{index:02d}.12345"
            )
        )

    importer_formulaire(
        document,
        formulaire,
    )

    traiter_document(
        document
    )

    sauver_calcul(
        document
    )

    #
    # Recherche publique
    #

    documents = rechercher_calculs(
        "2027",
        "0951",
        "11",
    )

    assert len(documents) >= 1

    for document in documents:

        assert (
            document["race"]["season"]
            == "2027"
        )

        assert (
            document["race"]["codex"]
            == "0951"
        )

        eet_index = document[
            "result"
        ]["eet_index"]

        competitor = document[
            "competitors"
        ][eet_index]

        assert competitor["bib"] == "11"

        assert competitor["eet_us"] is not None


def test_flux_a_saisie_mt_interface():
    """
    Vérifie le flux :

    système A
    -> création du calcul
    -> rappel par calculation_id
    -> saisie des MT par le formulaire
    -> calcul EET.
    """

    print()
    print(
        "TEST FLUX A + "
        "SAISIE MT INTERFACE"
    )

    #
    # Document EEP A
    #

    eep_a = {
        "race": {
            "season": "2027",
            "codex": "0951",
            "location": "Chamonix",
            "date": "2026-07-14",
            "discipline": "SL",
            "run": 1,
        },
        "competitors": [],
    }

    #
    # 10 ET de référence
    #

    for index in range(10):

        eep_a["competitors"].append(
            {
                "bib": str(
                    index + 1
                ),
                "et_tod": (
                    "10:00:"
                    f"{index:02d}.12345"
                ),
            }
        )

    #
    # Dossard avec ET manquant
    #

    eep_a["competitors"].append(
        {
            "bib": "11",
            "et_tod": None,
        }
    )

    #
    # Création par le système A
    #

    calculation_id = recevoir_eep(
        eep_a
    )

    assert calculation_id

    print(
        "OK - calcul créé :",
        calculation_id,
    )

    #
    # Rappel par calculation_id
    #

    document = rappeler_calcul(
        calculation_id
    )

    assert document is not None

    assert (
        document["info"]["calculation_id"]
        == calculation_id
    )

    print(
        "OK - calcul rappelé"
    )

    #
    # Simulation exacte des données
    # envoyées par le formulaire HTML
    #

    formulaire = {
        "precision_tm": "3",
        "dossard_eet": "11",
    }

    for index in range(11):

        formulaire[
            f"dossard_{index}"
        ] = str(
            index + 1
        )

        formulaire[
            f"tm_{index}"
        ] = (
            "10:00:"
            f"{index:02d}.223"
        )

        formulaire[
            f"te_{index}"
        ] = (
            ""
            if index == 10
            else (
                "10:00:"
                f"{index:02d}.12345"
            )
        )

    #
    # Même chemin que l'interface
    #

    importer_formulaire(
        document,
        formulaire,
    )

    traiter_document(
        document
    )

    #
    # Affichage des erreurs éventuelles
    #

    if document["info"]["errors"]:

        print(
            "ERREURS DOCUMENT :"
        )

        for erreur in document[
            "info"
        ]["errors"]:

            print(
                erreur
            )

    #
    # Vérification du résultat
    #

    eet_index = document[
        "result"
    ]["eet_index"]

    assert eet_index is not None

    competitor_eet = document[
        "competitors"
    ][eet_index]

    assert competitor_eet["bib"] == "11"

    assert competitor_eet["eet_tod"]

    assert document[
        "result"
    ]["reference_indexes"]

    print(
        "OK - MT saisies par formulaire"
    )

    print(
        "OK - EET calculé :",
        competitor_eet["eet_tod"],
    )


def test_eep():

    test_flux_eep()

    #
    # autres tests existants...
    #

    test_rechercher_calculs()
    test_recherche_criteres_facultatifs()
    test_flux_a_saisie_mt_interface()

    print(
        "Tous les tests EEP sont OK"
    )


def test_recherche_criteres_facultatifs():
    """
    Vérifie la recherche avec
    1, 2 ou 3 critères facultatifs.
    """

    print()
    print(
        "TEST RECHERCHE "
        "CRITERES FACULTATIFS"
    )

    #
    # Saison seule
    #

    documents = rechercher_calculs(
        "2027",
        "",
        "",
    )

    assert len(documents) >= 1

    for document in documents:

        assert (
            str(
                document["race"]["season"]
            )
            == "2027"
        )

    print(
        "OK - saison seule :",
        len(documents),
    )

    #
    # Codex seul
    #

    documents = rechercher_calculs(
        "",
        "0951",
        "",
    )

    assert len(documents) >= 1

    for document in documents:

        assert (
            str(
                document["race"]["codex"]
            )
            == "0951"
        )

    print(
        "OK - codex seul :",
        len(documents),
    )

    #
    # Dossard seul
    #

    documents = rechercher_calculs(
        "",
        "",
        "11",
    )

    assert len(documents) >= 1

    for document in documents:

        eet_index = document[
            "result"
        ]["eet_index"]

        competitor = document[
            "competitors"
        ][eet_index]

        assert (
            str(
                competitor["bib"]
            )
            == "11"
        )

    print(
        "OK - dossard seul :",
        len(documents),
    )

    #
    # Saison + Codex
    #

    documents = rechercher_calculs(
        "2027",
        "0951",
        "",
    )

    assert len(documents) >= 1

    for document in documents:

        assert (
            str(
                document["race"]["season"]
            )
            == "2027"
        )

        assert (
            str(
                document["race"]["codex"]
            )
            == "0951"
        )

    print(
        "OK - saison + codex :",
        len(documents),
    )

    #
    # Saison + Dossard
    #

    documents = rechercher_calculs(
        "2027",
        "",
        "11",
    )

    assert len(documents) >= 1

    for document in documents:

        assert (
            str(
                document["race"]["season"]
            )
            == "2027"
        )

        eet_index = document[
            "result"
        ]["eet_index"]

        competitor = document[
            "competitors"
        ][eet_index]

        assert (
            str(
                competitor["bib"]
            )
            == "11"
        )

    print(
        "OK - saison + dossard :",
        len(documents),
    )

    #
    # Codex + Dossard
    #

    documents = rechercher_calculs(
        "",
        "0951",
        "11",
    )

    assert len(documents) >= 1

    for document in documents:

        assert (
            str(
                document["race"]["codex"]
            )
            == "0951"
        )

        eet_index = document[
            "result"
        ]["eet_index"]

        competitor = document[
            "competitors"
        ][eet_index]

        assert (
            str(
                competitor["bib"]
            )
            == "11"
        )

    print(
        "OK - codex + dossard :",
        len(documents),
    )

    #
    # Saison + Codex + Dossard
    #

    documents = rechercher_calculs(
        "2027",
        "0951",
        "11",
    )

    assert len(documents) >= 1

    print(
        "OK - trois critères :",
        len(documents),
    )

    #
    # Aucun critère
    #

    documents = rechercher_calculs(
        "",
        "",
        "",
    )

    assert documents == []

    print(
        "OK - recherche vide refusée"
    )


if __name__ == "__main__":

    test_eep()
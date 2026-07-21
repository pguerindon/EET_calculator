"""
Tests du validateur des documents EEP.
"""

from services.eep_validator import (
    EEPValidationError,
    valider_eep_initial,
    valider_eep_secondaire,
)


# ============================================================================
# Documents de référence
# ============================================================================

def creer_eep_initial():
    """
    Crée un document EEP initial valide.
    """

    return {
        "calculation_id": "",
        "race": {
            "season": "2027",
            "codex": "0951",
            "run": 1,
            "missing_impulse": "FINISH",
        },
        "competitors": [
            {
                "bib": str(index + 1),
                "et_tod":
                    None if index == 10
                    else f"10:00:{index:02d}.12345",
            }
            for index in range(11)
        ],
    }


def creer_eep_secondaire():
    """
    Crée un document EEP secondaire valide.
    """

    return {
        "calculation_id": "ABC123",
        "race": {
            "season": "2027",
            "codex": "0951",
            "run": 1,
            "missing_impulse": "FINISH",
        },
        "competitors": [
            {
                "bib": str(index + 1),
                "et_tod": f"10:00:{index:02d}.12345",
            }
            for index in range(11)
        ],
    }


# ============================================================================
# Outil
# ============================================================================

def verifier_refus(document, fonction, message):

    try:

        fonction(document)

    except EEPValidationError:

        print("OK -", message)

        return

    raise AssertionError(message)


# ============================================================================
# Tests
# ============================================================================

def test_document_initial_valide():

    valider_eep_initial(
        creer_eep_initial()
    )

    print("OK - document initial valide")


def test_document_secondaire_valide():

    valider_eep_secondaire(
        creer_eep_secondaire()
    )

    print("OK - document secondaire valide")


def test_calculation_id_initial():

    document = creer_eep_initial()

    document["calculation_id"] = "ABC123"

    verifier_refus(
        document,
        valider_eep_initial,
        "calculation_id initial",
    )


def test_calculation_id_secondaire():

    document = creer_eep_secondaire()

    document["calculation_id"] = ""

    verifier_refus(
        document,
        valider_eep_secondaire,
        "calculation_id secondaire",
    )


def test_season():

    document = creer_eep_initial()

    document["race"]["season"] = "27"

    verifier_refus(
        document,
        valider_eep_initial,
        "season",
    )


def test_run():

    document = creer_eep_initial()

    document["race"]["run"] = 0

    verifier_refus(
        document,
        valider_eep_initial,
        "run minimum",
    )


def test_missing_impulse():

    document = creer_eep_initial()

    document["race"]["missing_impulse"] = "XXX"

    verifier_refus(
        document,
        valider_eep_initial,
        "missing_impulse",
    )


def test_competitor_count():

    document = creer_eep_initial()

    document["competitors"].pop()

    verifier_refus(
        document,
        valider_eep_initial,
        "nombre concurrents",
    )


def test_bib():

    document = creer_eep_initial()

    document["competitors"][0]["bib"] = 12

    verifier_refus(
        document,
        valider_eep_initial,
        "type bib",
    )


def test_et_tod():

    document = creer_eep_initial()

    document["competitors"][0]["et_tod"] = 123

    verifier_refus(
        document,
        valider_eep_initial,
        "type et_tod",
    )


def test_aucun_et_manquant():

    document = creer_eep_initial()

    document["competitors"][10]["et_tod"] = "10:00:10.12345"

    verifier_refus(
        document,
        valider_eep_initial,
        "aucun ET manquant",
    )


def test_deux_et_manquants():

    document = creer_eep_initial()

    document["competitors"][0]["et_tod"] = None

    verifier_refus(
        document,
        valider_eep_initial,
        "deux ET manquants",
    )


def test_et_manquant_secondaire():

    document = creer_eep_secondaire()

    document["competitors"][0]["et_tod"] = None

    verifier_refus(
        document,
        valider_eep_secondaire,
        "ET manquant secondaire",
    )


# ============================================================================
# Lance tous les tests
# ============================================================================

def test_eep_validator():

    print()
    print("===================================")
    print("TEST EEP VALIDATOR")
    print("===================================")

    test_document_initial_valide()
    test_document_secondaire_valide()

    test_calculation_id_initial()
    test_calculation_id_secondaire()

    test_season()
    test_run()
    test_missing_impulse()

    test_competitor_count()
    test_bib()
    test_et_tod()

    test_aucun_et_manquant()
    test_deux_et_manquants()
    test_et_manquant_secondaire()

    print()
    print("Tous les tests EEP Validator sont OK")


if __name__ == "__main__":

    test_eep_validator()
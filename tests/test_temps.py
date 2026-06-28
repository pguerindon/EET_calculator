"""
Tests du module temps.
"""

from services.temps import (
    tod_to_us,
    us_to_tod,
    duration_to_us,
    us_to_duration,
    arrondir_division_fis,
)


def test_temps():
    """
    Exécute tous les tests du module temps.
    """

    # ------------------------------------------------------------------
    # Tests des conversions TOD
    # ------------------------------------------------------------------

    assert tod_to_us("09:12:41.53082") == 33161530820
    assert us_to_tod(33161530820, 5) == "09:12:41.53082"

    # ------------------------------------------------------------------
    # Tests des conversions de durée
    # ------------------------------------------------------------------

    assert duration_to_us("0.16828") == 168280
    assert us_to_duration(168280, 5) == "0.16828"

    # ------------------------------------------------------------------
    # Tests de l'arrondi FIS
    # ------------------------------------------------------------------

    assert arrondir_division_fis(11574, 10) == 1157
    assert arrondir_division_fis(11575, 10) == 1158
    assert arrondir_division_fis(11576, 10) == 1158

    assert arrondir_division_fis(-11574, 10) == -1157
    assert arrondir_division_fis(-11575, 10) == -1158
    assert arrondir_division_fis(-11576, 10) == -1158

    assert arrondir_division_fis(0, 10) == 0

    print("Tous les tests de temps sont OK")


if __name__ == "__main__":

    test_temps()
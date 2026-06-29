"""
Lance tous les tests unitaires.
"""

from tests.test_temps import (
    test_temps,
)

from tests.test_import_json import (
    test_import_json,
)

from tests.test_calculator import (
    test_calculator,
)

from tests.test_validator import (
    test_validator,
)

from tests.test_adapter import (
    test_adapter,
)

def run_all_tests():
    """
    Exécute tous les tests.
    """

    print()
    print("----------------------------------------")
    print("Tests de EET Calculator")
    print("----------------------------------------")

    test_temps()

    test_import_json()

    test_calculator()

    test_validator()

    test_adapter()

    print("----------------------------------------")
    print("Tous les tests sont OK")
    print("----------------------------------------")
    print()


if __name__ == "__main__":

    run_all_tests()
"""
Lance tous les tests unitaires.
"""

from tests.test_calculator import (
    test_calculator,
)

from tests.test_document import (
    test_document,
)

from tests.test_document_store import (
    test_document_store,
)

from tests.test_eep_validator import (
    test_eep_validator,
)

from tests.test_temps import (
    test_temps,
)

from tests.test_translation import (
    test_translation,
)

from tests.test_validator import (
    test_validator,
)

from tests.test_workflow import (
    test_workflow,
)


def run_all_tests():
    """
    Exécute tous les tests.
    """

    print()
    print("----------------------------------------")
    print("Tests de EET Calculator")
    print("----------------------------------------")

    test_calculator()

    test_document()

    test_document_store()

    test_eep_validator()

    test_temps()

    test_translation()

    test_validator()

    test_workflow()

    print("----------------------------------------")
    print("Tous les tests sont OK")
    print("----------------------------------------")
    print()


if __name__ == "__main__":

    run_all_tests()
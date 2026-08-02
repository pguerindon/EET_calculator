#!/usr/bin/env python3
"""
Purge annuelle des calculs EET.

Supprime tous les calculs de la saison N-2
et enregistre un journal.
"""

from pathlib import Path
import sys
from datetime import datetime

#
# Ajoute la racine du projet au PYTHONPATH
#

PROJECT_DIR = (
    Path(__file__).resolve().parent.parent
)

sys.path.insert(
    0,
    str(PROJECT_DIR),
)

from services.document_store import (
    purger_documents,
)

#
# Répertoire des journaux
#

LOG_DIR = PROJECT_DIR / "logs"
LOG_DIR.mkdir(
    exist_ok=True
)

LOG_FILE = (
    LOG_DIR / "purge.log"
)


def main():
    """
    Lance la purge annuelle.
    """

    saison = str(
        datetime.now().year - 2
    )

    calculs_supprimes = (
        purger_documents(
            saison,
        )
    )

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8",
    ) as log:

        log.write(
            "=" * 60 + "\n"
        )

        log.write(
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S\n"
            )
        )

        log.write(
            f"Season purged : {saison}\n\n"
        )

        for calculation_id in calculs_supprimes:

            log.write(
                f"DELETE {calculation_id}\n"
            )

        log.write(
            f"\nDeleted : "
            f"{len(calculs_supprimes)}\n"
        )

        log.write(
            "=" * 60 + "\n\n"
        )

    print(
        f"{len(calculs_supprimes)} "
        f"calcul(s) de la saison "
        f"{saison} supprimé(s)."
    )


if __name__ == "__main__":
    main()
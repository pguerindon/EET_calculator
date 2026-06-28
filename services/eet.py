from decimal import Decimal
from decimal import ROUND_HALF_UP


def arrondi_fis_us(valeur_us: int, precision: int) -> int:
    """
    Arrondi FIS d'une valeur exprimée en microsecondes.

    Exemple :
        -115760 us -> -115800 us à 1/10000
        -115740 us -> -115700 us à 1/10000
    """

    secondes = Decimal(valeur_us) / Decimal("1000000")

    secondes_arrondies = secondes.quantize(
        Decimal("1." + ("0" * precision)),
        rounding=ROUND_HALF_UP
    )

    return int(secondes_arrondies * Decimal("1000000"))


def calcul_correction_us(
        deltas_us: list[int],
        precision_te: int
    ) -> int:

    somme = sum(deltas_us)

    moyenne = Decimal(somme) / Decimal(len(deltas_us))

    moyenne_us = int(moyenne)

    return tronquer_us(
        moyenne_us,
        precision_te
    )

def calcul_eet_us(
        tm_us: int,
        correction_us: int
    ) -> int:
    """
    EET = TM - Correction
    """

    return tm_us - correction_us


def tronquer_us(
        us: int,
        precision: int
    ) -> int:
    """
    Tronque une heure du jour à la précision demandée.
    """

    facteur = 10 ** (6 - precision)

    return (us // facteur) * facteur


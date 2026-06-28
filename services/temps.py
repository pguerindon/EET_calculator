from services import constants

def tod_to_us(tod: str) -> int:
    """
    Convertit HH:MM:SS.xxxxxx
    vers microsecondes depuis minuit.
    """

    if "." in tod:
        hms, frac = tod.split(".")
    else:
        hms = tod
        frac = "0"

    hh, mm, ss = map(
        int,
        hms.split(":")
    )

    if not (0 <= hh <= 23):
        raise ValueError(
            f"Heure invalide : {hh}"
        )

    if not (0 <= mm <= 59):
        raise ValueError(
            f"Minute invalide : {mm}"
        )

    if not (0 <= ss <= 59):
        raise ValueError(
            f"Seconde invalide : {ss}"
        )

    frac = frac.ljust(
        6,
        "0"
    )

    return (
        hh * 3600 * 1_000_000 +
        mm * 60 * 1_000_000 +
        ss * 1_000_000 +
        int(frac)
    )

def us_to_tod(us: int, precision: int = 6) -> str:

    hh = us // 3_600_000_000
    us %= 3_600_000_000

    mm = us // 60_000_000
    us %= 60_000_000

    ss = us // 1_000_000
    frac = us % 1_000_000

    frac_str = f"{frac:06d}"[:precision]

    return f"{hh:02d}:{mm:02d}:{ss:02d}.{frac_str}"

def delta_tod(tm: str, te: str) -> int:
    """
    Retourne TM - TE en microsecondes.
    """

    return tod_to_us(tm) - tod_to_us(te)


def us_to_delta(us: int, precision: int = 5) -> str:
    """
    Convertit un delta en microsecondes
    vers une chaîne affichable.

    Exemples :
        168280  -> 0.16828
       -80110  -> -0.08011
    """

    signe = ""

    if us < 0:
        signe = "-"
        us = abs(us)

    secondes = us / 1_000_000

    return f"{signe}{secondes:.{precision}f}"

def format_tm_fis(
    tod: str,
    precision_tm: int,
    precision_te: int
) -> str:

    precision_delta = max(
        precision_tm,
        precision_te
    )

    zeros = (
        precision_delta -
        precision_tm
    )

    if zeros <= 0:
        return tod

    return (
        tod +
        "(" +
        ("0" * zeros) +
        ")"
    )

def duration_to_us(
    duree
):
    """
    Convertit une durée en microsecondes.

    Exemples :
        0.16828
        62.5314
        -0.1157
    """

    signe = 1

    if duree.startswith("-"):
        signe = -1
        duree = duree[1:]

    if "." in duree:
        secondes, fraction = duree.split(".")
    else:
        secondes = duree
        fraction = "0"

    fraction = fraction.ljust(6, "0")

    return signe * (
        int(secondes) * 1_000_000
        + int(fraction[:6])
    )

def us_to_duration(
    us,
    precision
):
    """
    Convertit des microsecondes
    en durée.
    """

    signe = ""

    if us < 0:
        signe = "-"
        us = -us

    secondes = us // 1_000_000
    fraction = us % 1_000_000

    facteur = pas_precision(
        precision
    )

    fraction //= facteur

    return (
        f"{signe}"
        f"{secondes}."
        f"{fraction:0{precision}d}"
    )


def precision_tod(
    tod: str
) -> int:
    """
    Retourne le nombre de décimales
    d'un temps HH:MM:SS.xxxxxx.
    """

    if "." not in tod:
        return 0

    return len(
        tod.split(".")[1]
    )


def arrondir_us(
    temps_us,
    precision
):
    """
    Arrondit un temps à la précision demandée
    (arrondi classique).
    """

    pas = pas_precision(
        precision
    )

    return (
        (temps_us + pas // 2)
        // pas
    ) * pas


def tronquer_us(
    temps_us,
    precision
):
    """
    Tronque un temps à la précision demandée.
    """

    pas = pas_precision(
        precision
    )

    return (
        temps_us // pas
    ) * pas


def pas_precision(
    precision
):
    """
    Retourne le pas correspondant
    à une précision du chronomètre électronique.
    """

    return 10 ** (
        constants.MAX_ET_PRECISION - precision
    )


def arrondir_division_fis(
    dividende,
    diviseur
):
    """
    Retourne dividende / diviseur
    arrondi selon la règle FIS.

    Les calculs sont réalisés uniquement
    avec des entiers.

    L'arrondi est symétrique :
        5 ou plus -> valeur supérieure
        4 ou moins -> valeur inférieure
    """

    if diviseur <= 0:
        raise ValueError(
            "Le diviseur doit être strictement positif."
        )

    signe = 1

    if dividende < 0:

        signe = -1
        dividende = -dividende

    quotient = dividende // diviseur
    reste = dividende % diviseur

    if reste * 2 >= diviseur:

        quotient += 1

    return signe * quotient
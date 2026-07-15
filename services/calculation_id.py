"""
Génération et contrôle des identifiants de calcul.

Un calculation_id contient 6 caractères :

- 5 caractères représentant le nombre de secondes
  écoulées depuis le 1er janvier 2026, encodé en base 62 ;
- 1 caractère de contrôle.
"""

import time
from datetime import datetime


TOKEN_CHARS = (
    "0123456789"
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
)

CONTROL_WEIGHTS = (
    1,
    3,
    5,
    7,
    11,
)

TOKEN_LENGTH = 5

EPOCH_2026 = int(
    datetime(
        2026,
        1,
        1,
        0,
        0,
        0,
    ).timestamp()
)


def _encode_base62(n):
    """
    Encode un entier en base 62.
    """

    if n == 0:
        return TOKEN_CHARS[0].rjust(
            TOKEN_LENGTH,
            "0",
        )

    result = ""

    while n > 0:

        n, remainder = divmod(
            n,
            len(TOKEN_CHARS),
        )

        result = (
            TOKEN_CHARS[remainder]
            + result
        )

    return result.rjust(
        TOKEN_LENGTH,
        "0",
    )


def _calculer_caractere_controle(token):
    """
    Calcule le caractère de contrôle.
    """

    total = 0

    for caractere, poids in zip(
        token,
        CONTROL_WEIGHTS,
    ):

        valeur = TOKEN_CHARS.index(
            caractere
        )

        total += valeur * poids

    return TOKEN_CHARS[
        total % len(TOKEN_CHARS)
    ]


def generer_calculation_id():
    """
    Génère un nouvel identifiant de calcul.
    """

    offset = (
        int(time.time())
        - EPOCH_2026
    )

    token = _encode_base62(
        offset
    )

    controle = (
        _calculer_caractere_controle(
            token
        )
    )

    return token + controle


def verifier_calculation_id(calculation_id):
    """
    Vérifie le format et le caractère
    de contrôle d'un identifiant.
    """

    if not isinstance(
        calculation_id,
        str,
    ):
        return False

    if len(calculation_id) != (
        TOKEN_LENGTH + 1
    ):
        return False

    token = calculation_id[
        :TOKEN_LENGTH
    ]

    controle = calculation_id[
        TOKEN_LENGTH
    ]

    for caractere in calculation_id:

        if caractere not in TOKEN_CHARS:
            return False

    return (
        _calculer_caractere_controle(
            token
        )
        == controle
    )
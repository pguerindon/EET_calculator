from services.eet import (
    calcul_correction_us,
    calcul_eet_us,
    tronquer_us
)

from services.temps import (
    tod_to_us,
    us_to_tod
)

deltas = [
     225600,
    -173200,
       5800,
    -366400,
    -598800,
     -42700,
      51000,
    -125100,
    -181900,
      48100
]

correction = calcul_correction_us(
    deltas,
    4
)

print("Correction :", correction)

tm_manquant = tod_to_us(
    "10:07:51.5814"
)

eet = calcul_eet_us(
    tm_manquant,
    correction
)

eet = tronquer_us(
    eet,
    4
)

print(
    "EET :",
    us_to_tod(eet, 4)
)
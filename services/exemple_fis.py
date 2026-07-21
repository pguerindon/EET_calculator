"""
Jeux de données d'exemple EET Calculator.
"""

from services.temps import tod_to_us


def charger_exemple_fis(
    document,
):
    """
    Charge l'exemple officiel FIS
    dans un document existant.
    """

    race = document["race"]

    race["mt_precision"] = 4
    race["et_precision"] = 4

    donnees = [
        ("1",  "10:00:50.3548", "10:00:50.1292"),
        ("2",  "10:01:52.0189", "10:01:52.1921"),
        ("3",  "10:02:49.4978", "10:02:49.4920"),
        ("4",  "10:03:50.6148", "10:03:50.9812"),
        ("5",  "10:04:49.2741", "10:04:49.8729"),
        ("6",  "10:05:50.4702", "10:05:50.5129"),
        ("7",  "10:06:48.9125", "10:06:48.8615"),
        ("8",  "10:07:51.5814", None),
        ("9",  "10:08:49.8751", "10:08:50.0002"),
        ("10", "10:09:49.2459", "10:09:49.4278"),
        ("11", "10:10:50.3954", "10:10:50.3473"),
    ]

    competitors = document["competitors"]

    for competitor, (
        bib,
        mt_tod,
        et_tod,
    ) in zip(
        competitors,
        donnees,
    ):

        competitor["bib"] = bib

        competitor["mt_tod"] = mt_tod
        competitor["mt_us"] = tod_to_us(
            mt_tod
        )

        competitor["et_tod"] = et_tod

        if et_tod is not None:

            competitor["et_us"] = tod_to_us(
                et_tod
            )

        else:

            competitor["et_us"] = None
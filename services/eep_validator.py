"""
Validation des documents d'échange EEP.

Ce module valide la structure des documents
reçus des systèmes de chronométrage.

Il ne modifie aucune donnée.
"""
import re

from services.constants import (
    COMPETITOR_COUNT,
    COMPETITOR_SCHEMA,
    RACE_SCHEMA,
    ROOT_SCHEMA,
)


class EEPValidationError(Exception):
    """
    Erreur de validation d'un document EEP.
    """

    pass

def _valider_schema(
    data: dict,
    schema: dict,
) -> None:
    """
    Validate a dictionary against a schema.

    Args:
        data:
            Dictionary to validate.

        schema:
            Validation schema.

    Raises:
        EEPValidationError:
            If the dictionary does not conform to the schema.
    """

    for field, rules in schema.items():

        #
        # Mandatory / optional field
        #

        required = rules.get(
            "required",
            True,
        )

        if field not in data:

            if required:
                raise EEPValidationError(
                    f"Missing field '{field}'."
                )

            # Optional field absent
            continue

        value = data[field]

        #
        # Type
        #

        expected_type = rules.get("type")

        if (
            expected_type is not None
            and not isinstance(
                value,
                expected_type,
            )
        ):
            raise EEPValidationError(
                f"Invalid type for '{field}'."
            )

        #
        # Allowed values
        #

        allowed = rules.get("allowed")

        if (
            allowed is not None
            and value not in allowed
        ):
            raise EEPValidationError(
                f"Invalid value for '{field}'."
            )

        #
        # Regular expression
        #

        pattern = rules.get("pattern")

        if pattern is not None:

            if re.fullmatch(
                pattern,
                value,
            ) is None:
                raise EEPValidationError(
                    f"Invalid format for '{field}'."
                )

        #
        # Minimum
        #

        minimum = rules.get("minimum")

        if (
            minimum is not None
            and value < minimum
        ):
            raise EEPValidationError(
                f"'{field}' is below minimum value."
            )

        #
        # Maximum
        #

        maximum = rules.get("maximum")

        if (
            maximum is not None
            and value > maximum
        ):
            raise EEPValidationError(
                f"'{field}' exceeds maximum value."
            )
  

def valider_eep_initial(
    eep_document: dict,
) -> None:
    """
    Validate an initial EEP request.

    Args:
        eep_document:
            EEP document.

    Raises:
        EEPValidationError:
            If the document is invalid.
    """

    _valider_eep(
        eep_document,
    )

    #
    # Business rules
    #

    if eep_document["calculation_id"] != "":
        raise EEPValidationError(
            "calculation_id must be empty."
        )

    missing_count = sum(
        competitor["et_tod"].strip() == ""
        for competitor in eep_document["competitors"]
    )

    if missing_count != 1:
        raise EEPValidationError(
            "Exactly one missing ET is required."
        )


def valider_eep_secondaire(
    eep_document: dict,
) -> None:
    """
    Validate a secondary EEP request.

    Args:
        eep_document:
            EEP document.

    Raises:
        EEPValidationError:
            If the document is invalid.
    """

    _valider_eep(
        eep_document,
    )

    #
    # Business rules
    #

    if eep_document["calculation_id"] == "":
        raise EEPValidationError(
            "Missing calculation_id."
        )

    missing_count = sum(
        competitor["et_tod"] is None
        for competitor in eep_document["competitors"]
    )

    if missing_count != 0:
        raise EEPValidationError(
            "No missing ET is allowed."
        )
    

def _valider_eep(
    eep_document: dict,
) -> None:
    """
    Validate the common part of an EEP document.
    """

    _valider_document(
        eep_document,
    )

    _valider_race(
        eep_document["race"],
    )

    _valider_competitors(
        eep_document["competitors"],
    )
            

def _valider_document(
    eep_document: dict,
) -> None:
    """
    Validate the overall EEP document structure.

    Args:
        eep_document:
            EEP document.

    Raises:
        EEPValidationError:
            If the document structure is invalid.
    """

    if not isinstance(
        eep_document,
        dict,
    ):
        raise EEPValidationError(
            "Invalid EEP document."
        )

    _valider_schema(
        eep_document,
        ROOT_SCHEMA,
    )

    if not isinstance(
        eep_document["race"],
        dict,
    ):
        raise EEPValidationError(
            "Invalid race."
        )

    if not isinstance(
        eep_document["competitors"],
        list,
    ):
        raise EEPValidationError(
            "Invalid competitors."
        )
            

def _valider_race(
    race: dict,
) -> None:
    """
    Validate the race object.

    Args:
        race:
            Race object.

    Raises:
        EEPValidationError:
            If the race object is invalid.
    """

    if not isinstance(
        race,
        dict,
    ):
        raise EEPValidationError(
            "Invalid race."
        )

    _valider_schema(
        race,
        RACE_SCHEMA,
    )


def _valider_competitors(
    competitors: list,
) -> None:
    """
    Validate the competitors list.

    Args:
        competitors:
            Competitors list.

    Raises:
        EEPValidationError:
            If the competitors list is invalid.
    """

    if not isinstance(
        competitors,
        list,
    ):
        raise EEPValidationError(
            "Invalid competitors."
        )

    if len(
        competitors
    ) != COMPETITOR_COUNT:
        raise EEPValidationError(
            f"The EEP document must contain exactly {COMPETITOR_COUNT} competitors."
        )

    for competitor in competitors:

        if not isinstance(
            competitor,
            dict,
        ):
            raise EEPValidationError(
                "Invalid competitor."
            )

        _valider_schema(
            competitor,
            COMPETITOR_SCHEMA,
        )


"""
EEP protocol constants.

This module contains only static definitions:

- protocol validation schemas
- technical constants
- internal document models

No business logic belongs here.
"""
# ============================================================================
# constants.py
# ============================================================================

COPYRIGHT = "© 2026 Philippe Guérindon"

# ============================================================================
# Root document schema
# ============================================================================

ROOT_SCHEMA = {
    "calculation_id": {
        "type": str,
    },
    "race": {
        "type": dict,
    },
    "competitors": {
        "type": list,
    },
}

# ============================================================================
# Race object schema
# ============================================================================
# Valeurs autorisées pour missing_impulse:
# START  : impulsion de départ manquante (EEP)
# FINISH : impulsion d'arrivée manquante (EEP)
# WEB    : document créé par l'interface Web (interne uniquement)

RACE_SCHEMA = {
    "season": {
        "type": str,
        "pattern": r"^\d{4}$",
    },
    "codex": {
        "type": str,
    },
    "run": {
        "type": str,
        "allowed": (
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
        ),
    },
    "missing_impulse": {
        "type": str,
        "allowed": (
            "START",
            "FINISH",
            "WEB",
        ),
    },
    "eet_bib": {
        "type": str,
    },
    "location": {
        "type": str,
        "required": False,
    },
    "date": {
        "type": str,
        "required": False,
    },
    "discipline": {
        "type": str,
        "required": False,
    },
}

# ============================================================================
# Competitor object schema
# ============================================================================

COMPETITOR_SCHEMA = {
    "bib": {
        "type": str,
    },
    "et_tod": {
        "type": str,
    },
    "firstname": {
        "type": str,
        "required": False,
    },
    "lastname": {
        "type": str,
        "required": False,
    },
    "nation": {
        "type": str,
        "required": False,
    },
    "club": {
        "type": str,
        "required": False,
    },
}

# ============================================================================
# Protocol limits
# ============================================================================

COMPETITOR_COUNT = 11
REFERENCE_COMPETITOR_COUNT = 10

MIN_ET_PRECISION = 3
MAX_ET_PRECISION = 6

MIN_MT_PRECISION = 2
MAX_MT_PRECISION = 6

# ============================================================================
# Internal document models
# ============================================================================

INFO_MODEL = {
    "version": "",
    "errors": [],
}

RACE_MODEL = {
    "season": "",
    "codex": "",
    "location": "",
    "date": "",
    "discipline": "",
    "run": "1",
    "missing_impulse": "WEB",
    "eet_bib": "",
    "et_precision": None,
    "mt_precision": None,
}

COMPETITOR_MODEL = {
    "bib": "",

    "lastname": "",
    "firstname": "",
    "nation": "",
    "club": "",

    "et_tod": None,
    "et_us": None,

    "mt_tod": None,
    "mt_us": None,

    "delta_us": None,

    "eet_tod": None,
    "eet_us": None,
}

CALCULATION_MODEL = {
    "eet_index": None,
    "reference_indexes": [],
    "sum_delta_us": None,
    "correction_us": None,
}

DOCUMENT_MODEL = {
    "info": INFO_MODEL,
    "race": RACE_MODEL,
    "competitors": [],
    "calculation": CALCULATION_MODEL,
}

ERROR_MODEL = {
    "code": "",
    "field": "",
}
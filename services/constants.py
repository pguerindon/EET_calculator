# ----------------------------------------------------------------------
# Document
# ----------------------------------------------------------------------

DOCUMENT_VERSION = "1.0"


# ----------------------------------------------------------------------
# Statuts du document
# ----------------------------------------------------------------------

STATUS_NEW = "NEW"
STATUS_LOADED = "LOADED"
STATUS_VALIDATED = "VALIDATED"
STATUS_CALCULATED = "CALCULATED"
STATUS_ERROR = "ERROR"


# ----------------------------------------------------------------------
# Genres
# ----------------------------------------------------------------------

GENDER_MALE = "M"
GENDER_FEMALE = "F"
GENDER_ALL = "A"


# ----------------------------------------------------------------------
# Impulsion manquante
# ----------------------------------------------------------------------

IMPULSE_START = "start"
IMPULSE_FINISH = "finish"


# ----------------------------------------------------------------------
# Disciplines
# ----------------------------------------------------------------------

DISCIPLINE_SL = "SL"
DISCIPLINE_GS = "GS"
DISCIPLINE_SG = "SG"
DISCIPLINE_DH = "DH"
DISCIPLINE_AC = "AC"


# ----------------------------------------------------------------------
# Erreurs de validation
# ----------------------------------------------------------------------

ERROR_INVALID_COMPETITOR_COUNT = "INVALID_COMPETITOR_COUNT"
ERROR_DUPLICATE_BIB = "DUPLICATE_BIB"
ERROR_INVALID_ET_COUNT = "INVALID_ET_COUNT"
ERROR_INVALID_MISSING_IMPULSE = "INVALID_MISSING_IMPULSE"
ERROR_INVALID_ET_PRECISION = "INVALID_ET_PRECISION"
ERROR_INVALID_MT = "INVALID_MT"


# ----------------------------------------------------------------------
# Erreurs de calcul
# ----------------------------------------------------------------------

ERROR_NOT_ENOUGH_REFERENCES = "NOT_ENOUGH_REFERENCES"

# ----------------------------------------------------------------------
# Précision du chronomètre électronique
# ----------------------------------------------------------------------

MIN_ET_PRECISION = 3
MAX_ET_PRECISION = 6
DEFAULT_ET_PRECISION = 5

#
# Origine du document
#

ORIGIN_MANUAL = "manual"
ORIGIN_CHRONO = "chrono"

# ----------------------------------------------------------------------
# paramètres divers
# ----------------------------------------------------------------------

REFERENCE_COMPETITOR_COUNT = 10
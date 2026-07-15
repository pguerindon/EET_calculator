# config.py

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = "PG_CHRONO_EET_2026_SECRET_KEY"
DEBUG = False

SUPPORTED_LANGUAGES = ("fr", "en", "de")
DEFAULT_LANGUAGE = "en"

CALCULS_DIR = BASE_DIR / "calculs"
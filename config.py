# config.py

from pathlib import Path

import os

SECRET_KEY = os.environ["EET_SECRET_KEY"]


BASE_DIR = Path(__file__).resolve().parent

DEBUG = False

SUPPORTED_LANGUAGES = ("fr", "en", "de")
DEFAULT_LANGUAGE = "en"

CALCULS_DIR = BASE_DIR / "calculs"
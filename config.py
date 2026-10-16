from pathlib import Path
from datetime import timedelta

import os

SECRET_KEY = os.environ["EET_SECRET_KEY"]

ADMIN_SEARCH_CODE = os.environ["EET_ADMIN_SEARCH_CODE"]

PERMANENT_SESSION_LIFETIME = timedelta(hours=8)

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

BASE_DIR = Path(__file__).resolve().parent

DEBUG = False

SUPPORTED_LANGUAGES = ("fr", "en", "de")
DEFAULT_LANGUAGE = "en"

CALCULS_DIR = BASE_DIR / "calculs"
import os
from dotenv import load_dotenv

# take environment variables from .env.
load_dotenv()

APP_TITLE = os.getenv("APP_TITLE", "Geo-Lit")
APP_FAVICON = os.getenv("APP_FAVICON", "favicon.png")

SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
BOOKS_TAB_ID = os.environ["BOOKS_TAB_ID"]
EQUALITY_SCORES_TAB_ID = os.environ["EQUALITY_SCORES_TAB_ID"]
ABOUT_TAB_ID = os.environ["ABOUT_TAB_ID"]
ISO_CODES_TAB_ID = os.environ["ISO_CODES_TAB_ID"]

APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = os.getenv("APP_PORT", 8050)

PAGE_HEADER = "GÉOGRAPHIE LITTÉRAIRE FRANCOPHONE"

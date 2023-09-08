import os
from dotenv import load_dotenv

# take environment variables from .env.
load_dotenv()

APP_TITLE = os.getenv("APP_TITLE", "Geo-Lit")
APP_FAVICON = os.getenv("APP_FAVICON", "favicon.png")

APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = os.getenv("APP_PORT", 8050)

PAGE_HEADER = "GÉOGRAPHIE LITTÉRAIRE FRANCOPHONE"

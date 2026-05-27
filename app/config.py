from pathlib import Path

APP_TITLE = "ICAR ADE v1.5 API"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = (
    "REST API for ICAR Animal Data Exchange ADE v1.5 using FastAPI and TinyDB"
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
TINYDB_PATH = str(DATA_DIR / "tinydb.json")

DEFAULT_PAGE_LIMIT = 50
MAX_PAGE_LIMIT = 200

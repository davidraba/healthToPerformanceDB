from tinydb import TinyDB, Query
from app.config import TINYDB_PATH, DATA_DIR

DATA_DIR.mkdir(parents=True, exist_ok=True)

db = TinyDB(TINYDB_PATH, ensure_ascii=False, encoding="utf-8")


def get_table(resource_type: str):
    return db.table(resource_type)


def all_tables():
    return db.tables()


def drop_all():
    db.drop_tables()

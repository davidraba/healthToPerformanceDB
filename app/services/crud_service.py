from typing import Any, Dict, List, Optional
from tinydb import Query

from app.database import get_table
from app.utils.ids import generate_internal_id
from app.utils.dates import now_utc


def _doc(resource_type: str, payload: dict) -> dict:
    now = now_utc().isoformat()
    return {
        "internalId": generate_internal_id(),
        "resourceType": resource_type,
        "createdAt": now,
        "updatedAt": now,
        "payload": payload,
    }


def _update_timestamp(doc: dict) -> dict:
    doc["updatedAt"] = now_utc().isoformat()
    return doc


def create(resource_type: str, payload: dict) -> dict:
    table = get_table(resource_type)
    document = _doc(resource_type, payload)
    table.insert(document)
    return document


def get_by_id(resource_type: str, internal_id: str) -> Optional[dict]:
    table = get_table(resource_type)
    Elem = Query()
    result = table.get(Elem.internalId == internal_id)
    return result


def get_by_field(
    resource_type: str,
    field: str,
    value: Any,
) -> Optional[dict]:
    table = get_table(resource_type)
    Elem = Query()
    result = table.get(Elem.payload[field] == value)
    return result


def get_by_identifier(
    resource_type: str, scheme: str, animal_id: str
) -> Optional[dict]:
    table = get_table(resource_type)
    Elem = Query()
    result = table.get(
        (Elem.payload.identifier.scheme == scheme)
        & (Elem.payload.identifier.id == animal_id)
    )
    return result


def list_all(
    resource_type: str,
    limit: int = 50,
    offset: int = 0,
    filters: Optional[Dict[str, Any]] = None,
) -> tuple[List[dict], int]:
    table = get_table(resource_type)
    Elem = Query()
    docs = table.all()
    if filters:
        for key, value in filters.items():
            if key == "locationScheme":
                docs = [
                    d
                    for d in docs
                    if d.get("payload", {}).get("location", {}).get("scheme") == value
                ]
            elif key == "locationId":
                docs = [
                    d
                    for d in docs
                    if d.get("payload", {}).get("location", {}).get("id") == value
                ]
            elif key == "animalScheme":
                docs = [
                    d
                    for d in docs
                    if d.get("payload", {}).get("animal", {}).get("scheme") == value
                ]
            elif key == "animalId":
                docs = [
                    d
                    for d in docs
                    if d.get("payload", {}).get("animal", {}).get("id") == value
                ]
    total = len(docs)
    page = docs[offset : offset + limit]
    return page, total


def list_all_from_all_tables() -> tuple[List[dict], int]:
    from app.database import all_tables

    all_docs = []
    for table_name in all_tables():
        table = get_table(table_name)
        all_docs.extend(table.all())
    return all_docs, len(all_docs)


def update(resource_type: str, internal_id: str, payload: dict) -> Optional[dict]:
    table = get_table(resource_type)
    Elem = Query()
    existing = table.get(Elem.internalId == internal_id)
    if not existing:
        return None
    existing["payload"] = payload
    existing = _update_timestamp(existing)
    table.update(existing, Elem.internalId == internal_id)
    return existing


def patch(resource_type: str, internal_id: str, updates: dict) -> Optional[dict]:
    table = get_table(resource_type)
    Elem = Query()
    existing = table.get(Elem.internalId == internal_id)
    if not existing:
        return None
    existing["payload"].update(updates)
    existing = _update_timestamp(existing)
    table.update(existing, Elem.internalId == internal_id)
    return existing


def delete(resource_type: str, internal_id: str) -> bool:
    table = get_table(resource_type)
    Elem = Query()
    removed = table.remove(Elem.internalId == internal_id)
    return len(removed) > 0


def exists_by_identifier(resource_type: str, scheme: str, animal_id: str) -> bool:
    return get_by_identifier(resource_type, scheme, animal_id) is not None

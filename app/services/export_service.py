from typing import Any, Dict, List, Optional
from datetime import datetime

from app.database import all_tables, get_table


def _matches_filters(
    doc: Dict[str, Any],
    from_date: Optional[str],
    to_date: Optional[str],
    location_scheme: Optional[str],
    location_id: Optional[str],
) -> bool:
    payload = doc.get("payload", {})

    if location_scheme:
        loc = payload.get("location", {})
        if loc.get("scheme") != location_scheme:
            return False

    if location_id:
        loc = payload.get("location", {})
        if loc.get("id") != location_id:
            return False

    if from_date or to_date:
        event_dt = payload.get("eventDateTime") or payload.get("birthDate")
        if not event_dt:
            return False
        try:
            dt = datetime.fromisoformat(event_dt.replace("Z", "+00:00"))
            if from_date:
                fd = datetime.fromisoformat(from_date.replace("Z", "+00:00"))
                if dt < fd:
                    return False
            if to_date:
                td = datetime.fromisoformat(to_date.replace("Z", "+00:00"))
                if dt > td:
                    return False
        except (ValueError, TypeError):
            pass

    return True


def collect_documents(
    resource_type: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    location_scheme: Optional[str] = None,
    location_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    docs: List[Dict[str, Any]] = []

    if resource_type:
        tables = [resource_type] if resource_type in all_tables() else []
    else:
        tables = list(all_tables())

    for table_name in tables:
        table = get_table(table_name)
        for doc in table.all():
            if _matches_filters(doc, from_date, to_date, location_scheme, location_id):
                docs.append(doc)

    return docs


def _extract_coordinates(payload: Dict[str, Any]) -> Optional[List[float]]:
    lat = payload.get("latitude") or payload.get("lat")
    lng = payload.get("longitude") or payload.get("lng") or payload.get("long")
    if lat is not None and lng is not None:
        return [float(lng), float(lat)]

    position = payload.get("position") or payload.get("location", {})
    if isinstance(position, dict):
        lat = position.get("latitude") or position.get("lat")
        lng = position.get("longitude") or position.get("lng")
        if lat is not None and lng is not None:
            return [float(lng), float(lat)]

    return None


def _build_feature(doc: Dict[str, Any]) -> Dict[str, Any]:
    payload = doc.get("payload", {})
    internal_id = doc.get("internalId", "")
    resource_type = doc.get("resourceType", "")

    coordinates = _extract_coordinates(payload)

    properties = {
        "internalId": internal_id,
        "resourceType": resource_type,
        "createdAt": doc.get("createdAt", ""),
        "updatedAt": doc.get("updatedAt", ""),
    }
    for key, value in payload.items():
        if key not in ("latitude", "longitude", "lat", "lng", "position"):
            properties[key] = value

    feature: Dict[str, Any] = {
        "type": "Feature",
        "properties": properties,
    }

    if coordinates:
        feature["geometry"] = {
            "type": "Point",
            "coordinates": coordinates,
        }
    else:
        feature["geometry"] = None

    return feature


def build_geojson(documents: List[Dict[str, Any]]) -> Dict[str, Any]:
    features = [_build_feature(doc) for doc in documents]
    return {
        "type": "FeatureCollection",
        "features": features,
    }


def build_json_export(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return documents

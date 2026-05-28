from typing import Any, Dict, List, Type
from pydantic import ValidationError

from app.models import IcarResource
from app.services.resource_registry import resolve_model
from app.schemas.json_validator import validate_with_json_schema


def validate_payload(resource_type: str, payload: Dict[str, Any]) -> IcarResource:
    model_class: Type[IcarResource] = resolve_model(resource_type)
    try:
        validated = model_class(**payload)
    except ValidationError as e:
        raise e

    json_errors = validate_with_json_schema(resource_type, payload)
    if json_errors:
        detail = []
        for je in json_errors:
            detail.append({
                "type": "json_schema",
                "loc": (je["field"],),
                "msg": je["message"],
                "input": payload.get(je["field"]),
            })
        raise ValidationError.from_exception_data(
            "JSON Schema validation failed",
            line_errors=detail,
        )

    return validated

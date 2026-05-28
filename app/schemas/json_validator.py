from typing import Any, Dict, List, Optional
from functools import lru_cache

from jsonschema import ValidationError as JsonValidationError, Draft202012Validator
from pydantic import BaseModel

from app.services.resource_registry import resolve_model


_SCHEMA_CACHE: Dict[str, Optional[Dict[str, Any]]] = {}


def _pydantic_to_json_schema(model: type[BaseModel]) -> Dict[str, Any]:
    schema = model.model_json_schema()
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    schema["title"] = model.__name__
    return schema


def get_json_schema(resource_type: str) -> Optional[Dict[str, Any]]:
    if resource_type in _SCHEMA_CACHE:
        return _SCHEMA_CACHE[resource_type]

    model_class = resolve_model(resource_type)
    if model_class.__name__ == "GenericIcarResource":
        _SCHEMA_CACHE[resource_type] = None
        return None

    schema = _pydantic_to_json_schema(model_class)
    _SCHEMA_CACHE[resource_type] = schema
    return schema


def validate_with_json_schema(
    resource_type: str, payload: Dict[str, Any]
) -> List[Dict[str, Any]]:
    schema = get_json_schema(resource_type)
    if schema is None:
        return []

    validator = Draft202012Validator(schema)
    errors = []
    for error in sorted(validator.iter_errors(payload), key=str):
        field_path = ".".join(str(p) for p in error.absolute_path) if error.absolute_path else "root"
        errors.append({
            "field": field_path,
            "message": error.message,
        })
    return errors


def clear_schema_cache():
    _SCHEMA_CACHE.clear()

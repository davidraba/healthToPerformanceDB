from typing import Any, Dict
from datetime import datetime
from pydantic import BaseModel, Field

from .common import IcarMetaDataType


class GenericIcarResource(BaseModel):
    resourceType: str
    self_: str | None = Field(None, alias="@self")
    meta: IcarMetaDataType | None = None
    payload: Dict[str, Any]

    model_config = {"populate_by_name": True}

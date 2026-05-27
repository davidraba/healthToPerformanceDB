from typing import Optional, List
from pydantic import Field

from .common import IcarResource, IcarIdentifierType


class IcarAnimalSetResource(IcarResource):
    resourceType: str = Field(default="icarAnimalSetResource", alias="resourceType")
    name: Optional[str] = None
    members: Optional[List[IcarIdentifierType]] = None

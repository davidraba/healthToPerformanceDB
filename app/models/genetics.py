from typing import Optional
from pydantic import Field

from .common import IcarResource, IcarAnimalBaseResource


class IcarBreedingValueResource(IcarResource):
    resourceType: str = Field(default="icarBreedingValueResource", alias="resourceType")
    id: Optional[str] = None
    animal: Optional[dict] = None
    base: Optional[dict] = None
    version: Optional[str] = None
    breedingValues: Optional[list] = None


class IcarProgenyDetailsResource(IcarAnimalBaseResource):
    resourceType: str = Field(default="icarProgenyDetailsResource", alias="resourceType")
    identifier: Optional[dict] = None
    taggingDate: Optional[str] = None
    birthStatus: Optional[str] = None
    birthSize: Optional[str] = None
    birthWeight: Optional[float] = None

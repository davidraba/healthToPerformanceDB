from typing import Optional
from pydantic import Field

from .common import IcarResource, IcarAnimalEventCoreResource


class IcarCarcassResource(IcarResource):
    resourceType: str = Field(default="icarCarcassResource", alias="resourceType")
    id: Optional[str] = None
    weight: Optional[float] = None
    grade: Optional[str] = None
    category: Optional[str] = None


class IcarCarcassObservationsEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(default="icarCarcassObservationsEventResource", alias="resourceType")
    carcass: Optional[dict] = None
    observations: Optional[list] = None
    side: Optional[str] = None
    primal: Optional[str] = None
    carcassState: Optional[str] = None
    device: Optional[dict] = None

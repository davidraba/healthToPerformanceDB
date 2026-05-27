from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from .common import IcarIdentifierType, IcarResource


class IcarAnimalCoreResource(IcarResource):
    resourceType: str = Field(default="icarAnimalCoreResource", alias="resourceType")
    identifier: IcarIdentifierType
    alternativeIdentifiers: Optional[List[IcarIdentifierType]] = None
    specie: str
    gender: str
    birthDate: Optional[datetime] = None
    primaryBreed: Optional[IcarIdentifierType] = None
    breedFractions: Optional[dict] = None
    coatColor: Optional[str] = None
    managementTag: Optional[str] = None
    name: Optional[str] = None
    officialName: Optional[str] = None
    productionPurpose: Optional[str] = None
    status: Optional[str] = None
    reproductionStatus: Optional[str] = None
    lactationStatus: Optional[str] = None
    parentage: Optional[List[dict]] = None
    healthStatus: Optional[str] = None

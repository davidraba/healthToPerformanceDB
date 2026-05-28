from typing import Optional
from pydantic import Field

from .common import IcarResource, IcarAnimalEventCoreResource


class IcarObservationSummaryResource(IcarResource):
    resourceType: str = Field(default="icarObservationSummaryResource", alias="resourceType")
    animal: Optional[dict] = None
    statistics: Optional[list] = None


class IcarProcessingLotResource(IcarResource):
    resourceType: str = Field(default="icarProcessingLotResource", alias="resourceType")


class IcarStatisticsResource(IcarResource):
    resourceType: str = Field(default="icarStatisticsResource", alias="resourceType")
    id: Optional[str] = None
    location: Optional[dict] = None
    purpose: Optional[str] = None
    dateFrom: Optional[str] = None
    dateTo: Optional[str] = None
    group: Optional[list] = None


class IcarSchemeTypeResource(IcarResource):
    resourceType: str = Field(default="icarSchemeTypeResource", alias="resourceType")
    name: Optional[str] = None


class IcarSchemeValueResource(IcarResource):
    resourceType: str = Field(default="icarSchemeValueResource", alias="resourceType")
    id: Optional[str] = None
    name: Optional[str] = None


class IcarSortingSiteResource(IcarResource):
    resourceType: str = Field(default="icarSortingSiteResource", alias="resourceType")
    id: Optional[str] = None
    name: Optional[str] = None
    capacity: Optional[int] = None


class IcarAnimalSortingCommandResource(IcarResource):
    resourceType: str = Field(default="icarAnimalSortingCommandResource", alias="resourceType")
    animal: Optional[dict] = None
    sites: Optional[list] = None
    validFrom: Optional[str] = None
    validTo: Optional[str] = None


class IcarConformationScoreEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(default="icarConformationScoreEventResource", alias="resourceType")


class IcarTypeClassificationEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(default="icarTypeClassificationEventResource", alias="resourceType")
    conformationScores: Optional[list] = None

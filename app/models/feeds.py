from typing import Optional
from pydantic import Field

from .common import IcarResource, IcarAnimalEventCoreResource


class IcarFeedResource(IcarResource):
    resourceType: str = Field(default="icarFeedResource", alias="resourceType")
    id: Optional[str] = None
    category: Optional[str] = None
    type: Optional[dict] = None
    name: Optional[str] = None
    properties: Optional[list] = None
    active: Optional[bool] = None


class IcarFeedStorageResource(IcarResource):
    resourceType: str = Field(default="icarFeedStorageResource", alias="resourceType")
    id: Optional[str] = None
    serial: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    softwareVersion: Optional[str] = None
    hardwareVersion: Optional[str] = None
    isActive: Optional[bool] = None
    supportedMessages: Optional[list] = None
    manufacturer: Optional[dict] = None
    registration: Optional[dict] = None
    animal: Optional[dict] = None
    feedId: Optional[str] = None
    capacity: Optional[dict] = None
    quantityAvailable: Optional[dict] = None


class IcarFeedTransactionResource(IcarResource):
    resourceType: str = Field(default="icarFeedTransactionResource", alias="resourceType")
    quantity: Optional[float] = None
    unit: Optional[str] = None
    product: Optional[dict] = None


class IcarFeedIntakeEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(default="icarFeedIntakeEventResource", alias="resourceType")
    feedingStartingDateTime: Optional[str] = None
    feedVisitDuration: Optional[dict] = None
    consumedFeed: Optional[list] = None
    consumedRation: Optional[dict] = None
    device: Optional[dict] = None


class IcarFeedRecommendationResource(IcarResource):
    resourceType: str = Field(default="icarFeedRecommendationResource", alias="resourceType")
    id: Optional[str] = None
    animal: Optional[dict] = None
    recommendationDateTime: Optional[str] = None
    startDateTime: Optional[str] = None
    endDateTime: Optional[str] = None
    recommendedFeed: Optional[list] = None
    recommendedRation: Optional[list] = None


class IcarFeedReportResource(IcarResource):
    resourceType: str = Field(default="icarFeedReportResource", alias="resourceType")
    animals: Optional[list] = None
    reportStartDateTime: Optional[str] = None
    reportEndDateTime: Optional[str] = None
    feedVisitDuration: Optional[dict] = None
    consumedFeed: Optional[list] = None
    consumedRation: Optional[list] = None


class IcarRationResource(IcarResource):
    resourceType: str = Field(default="icarRationResource", alias="resourceType")
    id: Optional[str] = None
    name: Optional[str] = None
    feeds: Optional[list] = None
    active: Optional[bool] = None


class IcarGroupFeedingEventResource(IcarResource):
    resourceType: str = Field(default="icarGroupFeedingEventResource", alias="resourceType")
    id: Optional[str] = None
    eventDateTime: Optional[str] = None
    responsible: Optional[str] = None
    contemporaryGroup: Optional[str] = None
    remark: Optional[str] = None
    location: Optional[dict] = None
    groupMethod: Optional[str] = None
    countObserved: Optional[int] = None
    feedingEndDateTime: Optional[str] = None
    feedPerAnimal: Optional[list] = None
    feedTotal: Optional[list] = None
    rationPerAnimal: Optional[list] = None
    rationTotal: Optional[list] = None
    device: Optional[dict] = None

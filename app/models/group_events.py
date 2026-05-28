from typing import Optional
from pydantic import Field

from .common import IcarGroupEventCoreResource, IcarResource


class IcarGroupMovementBirthEventResource(IcarGroupEventCoreResource):
    resourceType: str = Field(default="icarGroupMovementBirthEventResource", alias="resourceType")
    registrationReason: Optional[str] = None


class IcarGroupMovementArrivalEventResource(IcarGroupEventCoreResource):
    resourceType: str = Field(default="icarGroupMovementArrivalEventResource", alias="resourceType")
    arrivalReason: Optional[str] = None
    consignment: Optional[dict] = None


class IcarGroupMovementDepartureEventResource(IcarGroupEventCoreResource):
    resourceType: str = Field(default="icarGroupMovementDepartureEventResource", alias="resourceType")
    departureKind: Optional[str] = None
    departureReason: Optional[str] = None
    consignment: Optional[dict] = None


class IcarGroupMovementDeathEventResource(IcarGroupEventCoreResource):
    resourceType: str = Field(default="icarGroupMovementDeathEventResource", alias="resourceType")
    deathreason: Optional[str] = None
    explanation: Optional[str] = None
    disposalMethod: Optional[str] = None
    disposalOperator: Optional[str] = None
    disposalReference: Optional[str] = None
    consignment: Optional[dict] = None
    deathMethod: Optional[str] = None


class IcarPositionObservationEventResource(IcarResource):
    resourceType: str = Field(default="icarPositionObservationEventResource", alias="resourceType")
    id: Optional[str] = None
    eventDateTime: Optional[str] = None
    responsible: Optional[str] = None
    contemporaryGroup: Optional[str] = None
    remark: Optional[str] = None
    location: Optional[dict] = None
    animal: Optional[dict] = None


class IcarGroupPositionObservationEventResource(IcarGroupEventCoreResource):
    resourceType: str = Field(default="icarGroupPositionObservationEventResource", alias="resourceType")

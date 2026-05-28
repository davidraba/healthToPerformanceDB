from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class IcarIdentifierType(BaseModel):
    scheme: str
    id: str


class IcarMetaDataType(BaseModel):
    source: Optional[str] = None
    sourceId: Optional[str] = None
    isDeleted: Optional[bool] = False
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
    creator: Optional[str] = None
    validFrom: Optional[datetime] = None
    validTo: Optional[datetime] = None


class IcarResource(BaseModel):
    resourceType: str
    self_: Optional[str] = Field(None, alias="@self")
    meta: Optional[IcarMetaDataType] = None
    location: Optional[IcarIdentifierType] = None

    model_config = {"populate_by_name": True}


class IcarEventCoreResource(IcarResource):
    id: Optional[str] = None
    eventDateTime: Optional[datetime] = None
    responsible: Optional[str] = None
    contemporaryGroup: Optional[str] = None
    remark: Optional[str] = None


class IcarAnimalEventCoreResource(IcarEventCoreResource):
    animal: IcarIdentifierType


class IcarAnimalBaseResource(BaseModel):
    identifier: IcarIdentifierType | None = None
    birthDate: datetime | None = None
    birthStatus: str | None = None
    birthSize: str | None = None
    birthWeight: float | None = None
    specie: str | None = None
    gender: str | None = None

    model_config = {"populate_by_name": True}


class IcarGroupEventCoreResource(IcarEventCoreResource):
    groupMethod: str | None = None
    countObserved: int | None = None
    inventoryClassification: dict | None = None
    embeddedAnimalSet: dict | None = None
    animalSetReference: dict | None = None

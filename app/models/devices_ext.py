from typing import Optional
from pydantic import Field

from .common import IcarResource


class IcarDeviceResource(IcarResource):
    resourceType: str = Field(default="icarDeviceResource", alias="resourceType")
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


class IcarMedicineResource(IcarResource):
    resourceType: str = Field(default="icarMedicineResource", alias="resourceType")
    name: Optional[str] = None
    approved: Optional[str] = None
    registeredID: Optional[dict] = None


class IcarMedicineTransactionResource(IcarResource):
    resourceType: str = Field(default="icarMedicineTransactionResource", alias="resourceType")
    quantity: Optional[float] = None
    unit: Optional[str] = None
    product: Optional[dict] = None


class IcarLocationResource(IcarResource):
    resourceType: str = Field(default="icarLocationResource", alias="resourceType")
    identifier: Optional[dict] = None
    alternativeIdentifiers: Optional[list] = None
    name: Optional[str] = None
    timeZoneId: Optional[str] = None


class IcarInventoryTransactionResource(IcarResource):
    resourceType: str = Field(default="icarInventoryTransactionResource", alias="resourceType")
    quantity: Optional[float] = None
    unit: Optional[str] = None
    product: Optional[dict] = None

import uuid

from pydantic import BaseModel

from app.models.address import AddressType


class AddressCreate(BaseModel):
    address_type: AddressType = AddressType.BHUTAN

    dzongkhag_id: uuid.UUID
    dungkhag_id: uuid.UUID
    gewog_id: uuid.UUID

    village: str

    additional_details: str | None = None


class AddressResponse(BaseModel):
    id: uuid.UUID

    address_type: AddressType

    dzongkhag_id: uuid.UUID
    dungkhag_id: uuid.UUID
    gewog_id: uuid.UUID

    village: str

    additional_details: str | None

    class Config:
        from_attributes = True
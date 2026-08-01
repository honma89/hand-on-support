import uuid

from pydantic import BaseModel

from app.models.address import AddressType


class DzongkhagResponse(BaseModel):
    id: uuid.UUID
    name: str

    class Config:
        from_attributes = True


class DungkhagResponse(BaseModel):
    id: uuid.UUID
    name: str
    dzongkhag_id: uuid.UUID

    class Config:
        from_attributes = True


class GewogResponse(BaseModel):
    id: uuid.UUID
    name: str
    dungkhag_id: uuid.UUID

    class Config:
        from_attributes = True


class AddressUpdate(BaseModel):
    address_type: AddressType = AddressType.BHUTAN

    dzongkhag_id: uuid.UUID | None = None
    dungkhag_id: uuid.UUID | None = None
    gewog_id: uuid.UUID | None = None
    village: str | None = None

    street_address: str | None = None
    address_line_2: str | None = None
    city: str | None = None
    state_province: str | None = None
    postal_code: str | None = None
    house_number: str | None = None
    landmark: str | None = None
    full_address: str | None = None


class AddressPublic(BaseModel):
    id: uuid.UUID
    address_type: AddressType

    dzongkhag_id: uuid.UUID | None
    dungkhag_id: uuid.UUID | None
    gewog_id: uuid.UUID | None
    village: str | None

    street_address: str | None
    address_line_2: str | None
    city: str | None
    state_province: str | None
    postal_code: str | None
    house_number: str | None
    landmark: str | None
    full_address: str | None

    class Config:
        from_attributes = True

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
    """Body for PUT /users/me/address."""

    address_type: AddressType = AddressType.BHUTAN

    dzongkhag_id: uuid.UUID
    dungkhag_id: uuid.UUID | None = None
    gewog_id: uuid.UUID

    village: str | None = None
    additional_details: str | None = None


class AddressPublic(BaseModel):
    id: uuid.UUID

    address_type: AddressType

    dzongkhag_id: uuid.UUID | None
    dungkhag_id: uuid.UUID | None
    gewog_id: uuid.UUID | None

    village: str | None
    full_address: str | None

    class Config:
        from_attributes = True

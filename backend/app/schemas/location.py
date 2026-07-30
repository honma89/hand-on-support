import uuid

from pydantic import BaseModel


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

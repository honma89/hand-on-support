import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.media import MediaType


class MediaCreate(BaseModel):
    title: str
    type: MediaType
    url: str


class MediaResponse(BaseModel):
    id: uuid.UUID
    title: str
    type: MediaType
    url: str
    uploaded_by: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True

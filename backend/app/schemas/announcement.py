import uuid
from datetime import datetime

from pydantic import BaseModel


class AnnouncementCreate(BaseModel):
    title: str
    content: str


class AnnouncementUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class AnnouncementResponse(BaseModel):
    id: uuid.UUID
    title: str
    content: str
    created_by: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True

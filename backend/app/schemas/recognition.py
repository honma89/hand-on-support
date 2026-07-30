import uuid
from datetime import datetime

from pydantic import BaseModel


class RecognitionCreate(BaseModel):
    user_id: uuid.UUID
    title: str
    description: str | None = None
    month: int
    year: int


class RecognitionResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    description: str | None
    month: int
    year: int
    created_at: datetime

    class Config:
        from_attributes = True

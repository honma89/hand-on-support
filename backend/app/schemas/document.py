import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.document import DocumentCategory


class DocumentCreate(BaseModel):
    title: str
    category: DocumentCategory
    file_url: str


class DocumentResponse(BaseModel):
    id: uuid.UUID
    title: str
    category: DocumentCategory
    file_url: str
    uploaded_by: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True

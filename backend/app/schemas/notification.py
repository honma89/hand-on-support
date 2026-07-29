import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import NotificationType


class NotificationPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    type: NotificationType
    title: str
    message: str
    is_read: bool
    related_entity_id: uuid.UUID | None
    created_at: datetime


class UnreadCountResponse(BaseModel):
    unread_count: int

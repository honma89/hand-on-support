import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import RegistrationStatus
from app.schemas.event import EventPublic
from app.schemas.user import UserPublic


class RegistrationPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    event_id: uuid.UUID
    user_id: uuid.UUID
    status: RegistrationStatus
    created_at: datetime


class RegistrationWithEvent(RegistrationPublic):
    event: EventPublic


class RegistrationWithUser(RegistrationPublic):
    user: UserPublic

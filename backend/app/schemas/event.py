import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.event import EventStatus
from app.models.event_registration import RegistrationStatus


class EventCreate(BaseModel):
    title: str
    description: str | None = None
    event_date: datetime
    department_id: uuid.UUID
    location_id: uuid.UUID | None = None
    max_volunteers: int | None = None
    points_reward: int = 0
    hours_reward: float = 0


class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    event_date: datetime | None = None
    location_id: uuid.UUID | None = None
    max_volunteers: int | None = None
    points_reward: int | None = None
    hours_reward: float | None = None
    status: EventStatus | None = None


class EventResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None
    event_date: datetime
    department_id: uuid.UUID
    location_id: uuid.UUID | None
    max_volunteers: int | None
    points_reward: int
    hours_reward: float
    status: EventStatus
    created_by: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


class EventRegistrationResponse(BaseModel):
    id: uuid.UUID
    event_id: uuid.UUID
    user_id: uuid.UUID
    status: RegistrationStatus
    registered_at: datetime

    class Config:
        from_attributes = True


class RegistrationStatusUpdate(BaseModel):
    status: RegistrationStatus

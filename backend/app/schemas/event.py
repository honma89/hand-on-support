import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import EventStatus


class EventCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str
    category: str = Field(max_length=100)
    dzongkhag: str = Field(max_length=100)
    location_detail: str | None = None
    start_datetime: datetime
    end_datetime: datetime
    capacity: int | None = None
    points_reward: int = 10
    status: EventStatus = EventStatus.DRAFT
    image_url: str | None = None
    location_id: uuid.UUID | None = None


class EventUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    description: str | None = None
    category: str | None = Field(default=None, max_length=100)
    dzongkhag: str | None = Field(default=None, max_length=100)
    location_detail: str | None = None
    start_datetime: datetime | None = None
    end_datetime: datetime | None = None
    capacity: int | None = None
    points_reward: int | None = None
    status: EventStatus | None = None
    image_url: str | None = None
    location_id: uuid.UUID | None = None


class EventPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    description: str
    category: str
    dzongkhag: str
    location_detail: str | None
    start_datetime: datetime
    end_datetime: datetime
    capacity: int | None
    points_reward: int
    status: EventStatus
    image_url: str | None
    organizer_id: uuid.UUID
    created_at: datetime


class EventDetail(EventPublic):
    registered_count: int
    spots_remaining: int | None

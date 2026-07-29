import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.enums import EventStatus
from app.schemas.user import UserPublic


class EventCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=10)
    category: str = Field(min_length=2, max_length=100)
    dzongkhag: str = Field(min_length=2, max_length=100)
    location_detail: str | None = Field(default=None, max_length=300)
    start_datetime: datetime
    end_datetime: datetime
    capacity: int | None = Field(default=None, gt=0)
    points_reward: int = Field(default=10, ge=0)
    image_url: str | None = Field(default=None, max_length=500)

    @field_validator("end_datetime")
    @classmethod
    def end_after_start(cls, v: datetime, info):
        start = info.data.get("start_datetime")
        if start and v <= start:
            raise ValueError("end_datetime must be after start_datetime")
        return v


class EventUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    description: str | None = Field(default=None, min_length=10)
    category: str | None = Field(default=None, min_length=2, max_length=100)
    dzongkhag: str | None = Field(default=None, min_length=2, max_length=100)
    location_detail: str | None = Field(default=None, max_length=300)
    start_datetime: datetime | None = None
    end_datetime: datetime | None = None
    capacity: int | None = Field(default=None, gt=0)
    points_reward: int | None = Field(default=None, ge=0)
    status: EventStatus | None = None
    image_url: str | None = Field(default=None, max_length=500)


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
    """Adds computed registration counts — used on the event detail page."""

    registered_count: int = 0
    spots_remaining: int | None = None

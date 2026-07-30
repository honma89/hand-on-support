import uuid
from datetime import datetime

from pydantic import BaseModel


class ActivityCategoryResponse(BaseModel):
    id: uuid.UUID
    name: str

    class Config:
        from_attributes = True


class ActivityResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    default_points: int
    default_hours: float
    activity_category_id: uuid.UUID

    class Config:
        from_attributes = True


class ActivityLogCreate(BaseModel):
    user_id: uuid.UUID
    activity_id: uuid.UUID
    event_id: uuid.UUID | None = None
    points_earned: int | None = None
    hours_logged: float | None = None


class ActivityLogResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    activity_id: uuid.UUID
    event_id: uuid.UUID | None
    points_earned: int
    hours_logged: float
    approved_by: uuid.UUID | None
    approved_at: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True

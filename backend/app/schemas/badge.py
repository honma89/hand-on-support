import uuid
from datetime import datetime

from pydantic import BaseModel


class BadgeResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    icon_url: str | None
    points_required: int

    class Config:
        from_attributes = True


class UserBadgeResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    badge_id: uuid.UUID
    earned_at: datetime

    class Config:
        from_attributes = True


class LeaderboardEntry(BaseModel):
    volunteer_id: uuid.UUID
    firstname: str
    lastname: str
    points_total: int
    hours_total: float

    class Config:
        from_attributes = True

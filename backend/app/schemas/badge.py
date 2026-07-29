import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import BadgeCriteriaType


class BadgeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=5, max_length=500)
    icon: str = Field(default="🏅", max_length=10)
    criteria_type: BadgeCriteriaType
    criteria_value: int = Field(gt=0)


class BadgePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str
    icon: str
    criteria_type: BadgeCriteriaType
    criteria_value: int


class UserBadgePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    badge_id: uuid.UUID
    awarded_at: datetime
    badge: BadgePublic

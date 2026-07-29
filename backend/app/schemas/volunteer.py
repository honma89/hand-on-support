import uuid
from datetime import date

from pydantic import BaseModel


class VolunteerCreate(BaseModel):
    firstname: str
    lastname: str
    date_of_birth: date | None = None
    gender: str | None = None
    phone_number: str
    telegram_username: str | None = None


class VolunteerResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID

    firstname: str
    lastname: str

    date_of_birth: date | None
    gender: str | None

    phone_number: str
    telegram_username: str | None

    points_total: int
    hours_total: float

    class Config:
        from_attributes = True
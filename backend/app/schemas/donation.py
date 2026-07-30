import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.models.donation import DonationStatus


class DonationCreate(BaseModel):
    phone_number: str
    donor_name: str
    email: EmailStr | None = None


class DonationResponse(BaseModel):
    id: uuid.UUID
    phone_number: str
    donor_name: str
    email: str | None
    payment_reference: str | None
    status: DonationStatus
    created_at: datetime

    class Config:
        from_attributes = True

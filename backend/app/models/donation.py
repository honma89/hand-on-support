import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import String, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.models.base import Base


class DonationStatus(str, PyEnum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class Donation(Base):
    __tablename__ = "donations"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    phone_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    donor_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    payment_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    status: Mapped[DonationStatus] = mapped_column(
        Enum(DonationStatus),
        default=DonationStatus.PENDING
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
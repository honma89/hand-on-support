import uuid
from datetime import datetime

from enum import Enum as PyEnum

from sqlalchemy import (
    Enum,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.models.base import Base


class RegistrationStatus(str, PyEnum):
    REGISTERED = "REGISTERED"
    ATTENDED = "ATTENDED"
    NO_SHOW = "NO_SHOW"
    CANCELLED = "CANCELLED"


class EventRegistration(Base):
    __tablename__ = "event_registrations"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    event_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("events.id"),
        nullable=False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    status: Mapped[RegistrationStatus] = mapped_column(
        Enum(RegistrationStatus),
        default=RegistrationStatus.REGISTERED
    )

    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
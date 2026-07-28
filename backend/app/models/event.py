import uuid
from datetime import datetime

from enum import Enum as PyEnum

from sqlalchemy import (
    String,
    Text,
    DateTime,
    Enum,
    Integer,
    ForeignKey
)

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.models.base import Base


class EventStatus(str, PyEnum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Event(Base):
    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    event_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    department_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("departments.id"),
        nullable=False
    )

    location_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("locations.id"),
        nullable=True
    )

    max_volunteers: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    points_reward: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    hours_reward: Mapped[float] = mapped_column(
        default=0
    )

    status: Mapped[EventStatus] = mapped_column(
        Enum(EventStatus),
        default=EventStatus.DRAFT
    )

    created_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
import uuid

from sqlalchemy import String, Text, Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    default_points: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    default_hours: Mapped[float] = mapped_column(
        Numeric,
        default=0
    )

    activity_category_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("activity_categories.id"),
        nullable=False
    )
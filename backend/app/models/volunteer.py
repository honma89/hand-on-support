import uuid
from datetime import date

from sqlalchemy import String, Integer, Numeric, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Volunteer(Base):
    __tablename__ = "volunteers"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    firstname: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    lastname: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    date_of_birth: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    gender: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    phone_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    address_id: Mapped[uuid.UUID | None] = mapped_column(
        nullable=True
    )

    telegram_username: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    points_total: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    hours_total: Mapped[float] = mapped_column(
        Numeric,
        default=0
    )

    tier_level_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("tier_levels.id"),
        nullable=True
    )
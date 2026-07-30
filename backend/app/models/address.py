import uuid

from sqlalchemy import String, Text, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from enum import Enum as PyEnum


class AddressType(str, PyEnum):
    BHUTAN = "BHUTAN"
    INTERNATIONAL = "INTERNATIONAL"


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    address_type: Mapped[AddressType] = mapped_column(
        Enum(AddressType),
        nullable=False
    )

    country_id: Mapped[uuid.UUID | None]

    dzongkhag_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("dzongkhags.id")
    )

    dungkhag_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("dungkhags.id")
    )

    gewog_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("gewogs.id")
    )

    village: Mapped[str | None] = mapped_column(String(100))

    street_address: Mapped[str | None] = mapped_column(Text)

    address_line_2: Mapped[str | None] = mapped_column(Text)

    city: Mapped[str | None] = mapped_column(String(100))

    state_province: Mapped[str | None] = mapped_column(String(100))

    postal_code: Mapped[str | None] = mapped_column(String(20))

    house_number: Mapped[str | None] = mapped_column(String(50))

    landmark: Mapped[str | None] = mapped_column(Text)

    full_address: Mapped[str | None] = mapped_column(Text)

    volunteer = relationship(
        "Volunteer",
        back_populates="address",
        uselist=False
    )
import uuid
from enum import StrEnum

from sqlalchemy import String, Text, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.mixins import TimestampMixin
from app.db.session import Base


class AddressType(StrEnum):
    BHUTAN = "bhutan"
    INTERNATIONAL = "international"


class Address(Base, TimestampMixin):
    __tablename__ = "addresses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    address_type: Mapped[AddressType] = mapped_column(Enum(AddressType, name="address_type"), nullable=False)

    # Bhutan administrative hierarchy (nullable — only applies when address_type == BHUTAN)
    dzongkhag_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("dzongkhags.id", ondelete="SET NULL"), nullable=True
    )
    dungkhag_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("dungkhags.id", ondelete="SET NULL"), nullable=True
    )
    gewog_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("gewogs.id", ondelete="SET NULL"), nullable=True
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

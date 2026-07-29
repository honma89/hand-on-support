import uuid
from enum import StrEnum

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
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
    village: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # International / free-form fallback fields
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    state_province: Mapped[str | None] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[str | None] = mapped_column(String(20), nullable=True)

    street_address: Mapped[str | None] = mapped_column(Text, nullable=True)
    address_line_2: Mapped[str | None] = mapped_column(Text, nullable=True)
    house_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    landmark: Mapped[str | None] = mapped_column(Text, nullable=True)
    full_address: Mapped[str | None] = mapped_column(Text, nullable=True)

    dzongkhag: Mapped["Dzongkhag"] = relationship()
    dungkhag: Mapped["Dungkhag"] = relationship()
    gewog: Mapped["Gewog"] = relationship()

    def __repr__(self) -> str:
        return f"<Address {self.address_type} {self.full_address or ''}>"

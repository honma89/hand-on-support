import uuid
from enum import StrEnum

from sqlalchemy import Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.mixins import TimestampMixin
from app.db.session import Base


class DonationStatus(StrEnum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class Donation(Base, TimestampMixin):
    """Standalone donor record — intentionally not linked to `users`, since
    donors are not required to have an account."""

    __tablename__ = "donations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    donor_name: Mapped[str] = mapped_column(String(150), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    payment_reference: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[DonationStatus] = mapped_column(
        Enum(DonationStatus, name="donation_status"), nullable=False, default=DonationStatus.PENDING
    )

    def __repr__(self) -> str:
        return f"<Donation {self.donor_name} ({self.status})>"

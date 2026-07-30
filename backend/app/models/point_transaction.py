import uuid

from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.mixins import TimestampMixin
from app.db.session import Base
from app.models.enums import PointTransactionType


class PointTransaction(Base, TimestampMixin):
    """
    Append-only ledger of every point movement. A user's balance is always
    SUM(amount) over their transactions — we deliberately never store a
    cached balance column, so the numbers can never drift out of sync.
    """

    __tablename__ = "point_transactions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    event_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("events.id", ondelete="SET NULL"), nullable=True
    )

    # Positive for EARNED/BONUS, negative for REDEEMED, either sign for ADJUSTMENT.
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[PointTransactionType] = mapped_column(
        Enum(PointTransactionType, name="point_transaction_type"), nullable=False
    )
    description: Mapped[str] = mapped_column(String(300), nullable=False)

    created_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    user: Mapped["User"] = relationship(back_populates="point_transactions", foreign_keys=[user_id])
    event: Mapped["Event"] = relationship()
    created_by: Mapped["User"] = relationship(foreign_keys=[created_by_id])

    def __repr__(self) -> str:
        return f"<PointTransaction user={self.user_id} amount={self.amount} type={self.type}>"

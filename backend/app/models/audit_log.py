import uuid
from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.models.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    action_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    entity_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    entity_id: Mapped[uuid.UUID | None]

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    log_metadata: Mapped[dict | None] = mapped_column(
    "metadata",
    JSON,
    nullable=True
    )
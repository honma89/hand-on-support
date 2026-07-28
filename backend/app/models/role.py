import uuid
from enum import Enum as PyEnum

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class RoleName(str, PyEnum):
    ADMIN = "ADMIN"
    VOLUNTEER = "VOLUNTEER"


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    name: Mapped[RoleName] = mapped_column(
        Enum(RoleName),
        nullable=False,
        unique=True
    )
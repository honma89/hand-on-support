import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import RegistrationStatus
from app.models.event_registration import EventRegistration


class RegistrationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, registration_id: uuid.UUID) -> EventRegistration | None:
        return await self.db.get(EventRegistration, registration_id)

    async def get_by_event_and_user(
        self, event_id: uuid.UUID, user_id: uuid.UUID
    ) -> EventRegistration | None:
        result = await self.db.execute(
            select(EventRegistration).where(
                EventRegistration.event_id == event_id,
                EventRegistration.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def create(self, registration: EventRegistration) -> EventRegistration:
        self.db.add(registration)
        await self.db.flush()
        await self.db.refresh(registration)
        return registration

    async def save(self, registration: EventRegistration) -> EventRegistration:
        await self.db.flush()
        await self.db.refresh(registration)
        return registration

    async def list_for_user(self, user_id: uuid.UUID) -> list[EventRegistration]:
        result = await self.db.execute(
            select(EventRegistration)
            .where(EventRegistration.user_id == user_id)
            .order_by(EventRegistration.created_at.desc())
        )
        return list(result.scalars().all())

    async def list_for_event(
        self, event_id: uuid.UUID, status: RegistrationStatus | None = None
    ) -> list[EventRegistration]:
        query = select(EventRegistration).where(EventRegistration.event_id == event_id)
        if status:
            query = query.where(EventRegistration.status == status)
        result = await self.db.execute(query.order_by(EventRegistration.created_at.asc()))
        return list(result.scalars().all())

    async def get_earliest_waitlisted(self, event_id: uuid.UUID) -> EventRegistration | None:
        result = await self.db.execute(
            select(EventRegistration)
            .where(
                EventRegistration.event_id == event_id,
                EventRegistration.status == RegistrationStatus.WAITLISTED,
            )
            .order_by(EventRegistration.created_at.asc())
            .limit(1)
        )
        return result.scalar_one_or_none()

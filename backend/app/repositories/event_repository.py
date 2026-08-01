import uuid

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import EventStatus, RegistrationStatus
from app.models.event import Event
from app.models.event_registration import EventRegistration


class EventRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, event_id: uuid.UUID) -> Event | None:
        return await self.db.get(Event, event_id)

    async def create(self, event: Event) -> Event:
        self.db.add(event)
        await self.db.flush()
        await self.db.refresh(event)
        return event

    async def save(self, event: Event) -> Event:
        await self.db.flush()
        await self.db.refresh(event)
        return event

    async def delete(self, event: Event) -> None:
        await self.db.delete(event)
        await self.db.flush()

    async def list_filtered(
        self,
        status: EventStatus | None = None,
        category: str | None = None,
        dzongkhag: str | None = None,
        upcoming_only: bool = False,
        organizer_id: uuid.UUID | None = None,
        visible_to_owner_id: uuid.UUID | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Event]:
        query = select(Event)

        if organizer_id:
            # Scoped to exactly one organizer's events (any status) --
            # used for an organizer's own "My Events" list, or an admin
            # filtering the admin list down to a specific organizer.
            query = query.where(Event.organizer_id == organizer_id)
        elif visible_to_owner_id:
            # An organizer's default "coordination" view: every published
            # event from any organizer, PLUS their own events regardless
            # of status (their drafts/cancelled remain visible to them).
            # If a status filter was also requested, it narrows the
            # "anyone's events" branch; their own events stay visible
            # either way.
            published_branch = Event.status == (status or EventStatus.PUBLISHED)
            own_branch = Event.organizer_id == visible_to_owner_id
            query = query.where(or_(published_branch, own_branch))
        elif status:
            query = query.where(Event.status == status)

        if category:
            query = query.where(Event.category == category)
        if dzongkhag:
            query = query.where(Event.dzongkhag == dzongkhag)
        if upcoming_only:
            query = query.where(Event.start_datetime >= func.now())

        query = query.order_by(Event.start_datetime.asc()).offset(offset).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count_active_registrations(self, event_id: uuid.UUID) -> int:
        query = select(func.count()).select_from(EventRegistration).where(
            EventRegistration.event_id == event_id,
            EventRegistration.status == RegistrationStatus.REGISTERED,
        )
        result = await self.db.execute(query)
        return int(result.scalar_one())

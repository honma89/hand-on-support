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
        q: str | None = None,
        sort_by: str = "soonest",
        offset: int = 0,
        limit: int = 20,
    ) -> list[Event]:
        query = select(Event)
        if status:
            query = query.where(Event.status == status)
        if category:
            query = query.where(Event.category == category)
        if dzongkhag:
            query = query.where(Event.dzongkhag == dzongkhag)
        if upcoming_only:
            query = query.where(Event.start_datetime >= func.now())
        if organizer_id:
            query = query.where(Event.organizer_id == organizer_id)
        if q:
            like = f"%{q}%"
            query = query.where(
                or_(
                    Event.title.ilike(like),
                    Event.description.ilike(like),
                    Event.category.ilike(like),
                )
            )

        if sort_by == "popular":
            registered_count = (
                select(func.count())
                .select_from(EventRegistration)
                .where(
                    EventRegistration.event_id == Event.id,
                    EventRegistration.status == RegistrationStatus.REGISTERED,
                )
                .correlate(Event)
                .scalar_subquery()
            )
            query = query.order_by(registered_count.desc(), Event.start_datetime.asc())
        elif sort_by == "newest":
            query = query.order_by(Event.created_at.desc())
        else:  # "soonest" (default)
            query = query.order_by(Event.start_datetime.asc())

        query = query.offset(offset).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def list_similar(self, event: Event, limit: int = 5) -> list[Event]:
        """Other upcoming, published events in the same category - falls
        back to the same dzongkhag if nothing else matches the category."""
        base_query = select(Event).where(
            Event.id != event.id,
            Event.status == EventStatus.PUBLISHED,
            Event.start_datetime >= func.now(),
        )

        by_category = await self.db.execute(
            base_query.where(Event.category == event.category)
            .order_by(Event.start_datetime.asc())
            .limit(limit)
        )
        matches = list(by_category.scalars().all())
        if len(matches) >= limit:
            return matches

        seen_ids = {e.id for e in matches}
        by_location = await self.db.execute(
            base_query.where(Event.dzongkhag == event.dzongkhag)
            .order_by(Event.start_datetime.asc())
            .limit(limit)
        )
        for e in by_location.scalars().all():
            if e.id not in seen_ids:
                matches.append(e)
                seen_ids.add(e.id)
            if len(matches) >= limit:
                break

        return matches[:limit]

    async def count_active_registrations(self, event_id: uuid.UUID) -> int:
        query = select(func.count()).select_from(EventRegistration).where(
            EventRegistration.event_id == event_id,
            EventRegistration.status == RegistrationStatus.REGISTERED,
        )
        result = await self.db.execute(query)
        return int(result.scalar_one())

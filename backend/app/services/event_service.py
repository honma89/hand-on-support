import uuid

from app.core.exceptions import ForbiddenError, NotFoundError
from app.models.enums import EventStatus, UserRole
from app.models.event import Event
from app.models.user import User
from app.repositories.event_repository import EventRepository
from app.schemas.event import EventCreate, EventDetail, EventPublic, EventUpdate


class EventService:
    def __init__(self, event_repo: EventRepository):
        self.event_repo = event_repo

    async def get_or_raise(self, event_id: uuid.UUID) -> Event:
        event = await self.event_repo.get_by_id(event_id)
        if not event:
            raise NotFoundError("Event not found.")
        return event

    async def get_detail(self, event_id: uuid.UUID) -> EventDetail:
        event = await self.get_or_raise(event_id)
        return await self._to_detail(event)

    async def _to_detail(self, event: Event) -> EventDetail:
        registered_count = await self.event_repo.count_active_registrations(event.id)
        spots_remaining = (
            max(event.capacity - registered_count, 0) if event.capacity is not None else None
        )
        base = EventPublic.model_validate(event)
        return EventDetail(
            **base.model_dump(),
            registered_count=registered_count,
            spots_remaining=spots_remaining,
        )

    async def create(self, data: EventCreate, organizer: User) -> Event:
        event = Event(**data.model_dump(), organizer_id=organizer.id, status=EventStatus.DRAFT)
        return await self.event_repo.create(event)

    def _assert_can_manage(self, event: Event, actor: User) -> None:
        if actor.role == UserRole.ADMIN:
            return
        if actor.role == UserRole.ORGANIZER and event.organizer_id == actor.id:
            return
        raise ForbiddenError("You do not have permission to manage this event.")

    async def update(self, event_id: uuid.UUID, data: EventUpdate, actor: User) -> Event:
        event = await self.get_or_raise(event_id)
        self._assert_can_manage(event, actor)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(event, field, value)
        return await self.event_repo.save(event)

    async def delete(self, event_id: uuid.UUID, actor: User) -> None:
        event = await self.get_or_raise(event_id)
        self._assert_can_manage(event, actor)
        await self.event_repo.delete(event)

    async def list_events(
        self,
        status: EventStatus | None,
        category: str | None,
        dzongkhag: str | None,
        upcoming_only: bool,
        offset: int,
        limit: int,
    ) -> list[Event]:
        return await self.event_repo.list_filtered(
            status=status,
            category=category,
            dzongkhag=dzongkhag,
            upcoming_only=upcoming_only,
            offset=offset,
            limit=limit,
        )

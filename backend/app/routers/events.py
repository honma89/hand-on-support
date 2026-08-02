import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ForbiddenError, NotFoundError
from app.db.session import get_db
from app.deps import CurrentUser, CurrentUserOptional, require_organizer_or_admin
from app.models.enums import EventStatus, UserRole
from app.repositories.address_repository import AddressRepository
from app.repositories.event_repository import EventRepository
from app.schemas.event import EventCreate, EventDetail, EventPublic, EventUpdate
from app.services.event_service import EventService

router = APIRouter(prefix="/events", tags=["events"])


def get_event_service(db: AsyncSession = Depends(get_db)) -> EventService:
    return EventService(EventRepository(db), address_repo=AddressRepository(db))


@router.get("", response_model=list[EventPublic])
async def list_events(
    current_user: CurrentUserOptional,
    status_filter: EventStatus | None = Query(default=None, alias="status"),
    category: str | None = None,
    dzongkhag: str | None = None,
    upcoming_only: bool = False,
    organizer_id: uuid.UUID | None = None,
    q: str | None = Query(default=None, description="Keyword search across title/description/category"),
    sort_by: str = Query(default="soonest", pattern="^(soonest|popular|newest)$"),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    service: EventService = Depends(get_event_service),
):
    # Draft/cancelled events are only visible to their own organizer or an
    # admin. Anonymous visitors and volunteers always get published-only,
    # regardless of what status filter they ask for -- otherwise anyone
    # could see unpublished events by omitting/forging the status param.
    is_admin = current_user is not None and current_user.role == UserRole.ADMIN
    is_owning_organizer = (
        current_user is not None
        and current_user.role == UserRole.ORGANIZER
        and organizer_id is not None
        and organizer_id == current_user.id
    )

    if not (is_admin or is_owning_organizer):
        status_filter = EventStatus.PUBLISHED

    return await service.list_events(
        status=status_filter,
        category=category,
        dzongkhag=dzongkhag,
        upcoming_only=upcoming_only,
        organizer_id=organizer_id,
        q=q,
        sort_by=sort_by,
        offset=offset,
        limit=limit,
    )


@router.get("/near-me", response_model=list[EventPublic])
async def list_events_near_me(
    current_user: CurrentUser,
    limit: int = Query(default=20, ge=1, le=100),
    service: EventService = Depends(get_event_service),
):
    """Upcoming, published events in the caller's saved dzongkhag. Returns
    an empty list rather than an error if they haven't set an address yet."""
    return await service.get_events_near_me(current_user, limit=limit)


@router.get("/{event_id}", response_model=EventDetail)
async def get_event(event_id: uuid.UUID, service: EventService = Depends(get_event_service)):
    try:
        return await service.get_event_detail(event_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.get("/{event_id}/similar", response_model=list[EventPublic])
async def get_similar_events(
    event_id: uuid.UUID,
    limit: int = Query(default=5, ge=1, le=20),
    service: EventService = Depends(get_event_service),
):
    """Other upcoming events worth showing on this event's detail page -
    same category first, same dzongkhag as a fallback."""
    try:
        return await service.get_similar_events(event_id, limit=limit)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.post(
    "",
    response_model=EventPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_organizer_or_admin)],
)
async def create_event(
    data: EventCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    service: EventService = Depends(get_event_service),
):
    event = await service.create_event(data, current_user)
    await db.commit()
    return event


@router.patch(
    "/{event_id}",
    response_model=EventPublic,
    dependencies=[Depends(require_organizer_or_admin)],
)
async def update_event(
    event_id: uuid.UUID,
    data: EventUpdate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    service: EventService = Depends(get_event_service),
):
    try:
        event = await service.update_event(event_id, data, current_user)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    await db.commit()
    return event


@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_organizer_or_admin)],
)
async def delete_event(
    event_id: uuid.UUID,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    service: EventService = Depends(get_event_service),
):
    try:
        await service.delete_event(event_id, current_user)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    await db.commit()

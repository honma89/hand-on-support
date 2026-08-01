import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ForbiddenError, NotFoundError
from app.db.session import get_db
from app.deps import CurrentUser, CurrentUserOptional, require_organizer_or_admin
from app.models.enums import EventStatus, UserRole
from app.repositories.event_repository import EventRepository
from app.schemas.event import EventCreate, EventDetail, EventPublic, EventUpdate
from app.services.event_service import EventService

router = APIRouter(prefix="/events", tags=["events"])


def get_event_service(db: AsyncSession = Depends(get_db)) -> EventService:
    return EventService(EventRepository(db))


@router.get("", response_model=list[EventPublic])
async def list_events(
    current_user: CurrentUserOptional,
    status_filter: EventStatus | None = Query(default=None, alias="status"),
    category: str | None = None,
    dzongkhag: str | None = None,
    upcoming_only: bool = False,
    organizer_id: uuid.UUID | None = None,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    service: EventService = Depends(get_event_service),
):
    # Visibility rules (separate from _assert_can_manage, which governs
    # who can *edit* an event -- this only governs who can *see* one):
    #
    # - Admin: unrestricted, any status/organizer filter honored as-is.
    # - Organizer, explicit organizer_id == self: pure "my events" view,
    #   any status, since it's unambiguously their own request.
    # - Organizer, no organizer_id (or someone else's): "coordination"
    #   view -- every published event from any organizer, PLUS their own
    #   regardless of status. They still can't see another organizer's
    #   drafts/cancelled even if they pass that organizer's id.
    # - Anonymous/volunteer: published-only, always, regardless of what
    #   they ask for (prevents seeing unpublished events by omitting or
    #   forging the status/organizer_id params).
    is_admin = current_user is not None and current_user.role == UserRole.ADMIN
    is_organizer = current_user is not None and current_user.role == UserRole.ORGANIZER
    is_own_organizer_id = is_organizer and organizer_id is not None and organizer_id == current_user.id

    visible_to_owner_id: uuid.UUID | None = None
    effective_organizer_id = organizer_id

    if is_admin:
        pass  # no restriction
    elif is_own_organizer_id:
        pass  # organizer_id already scopes to exactly their own events
    elif is_organizer:
        # Coordination view: ignore any (possibly other-organizer's) id
        # they passed for visibility purposes -- they only ever get
        # published-from-anyone plus their own.
        effective_organizer_id = None
        visible_to_owner_id = current_user.id
    else:
        # Anonymous or volunteer.
        status_filter = EventStatus.PUBLISHED

    return await service.list_events(
        status=status_filter,
        category=category,
        dzongkhag=dzongkhag,
        upcoming_only=upcoming_only,
        organizer_id=effective_organizer_id,
        visible_to_owner_id=visible_to_owner_id,
        offset=offset,
        limit=limit,
    )


@router.get("/{event_id}", response_model=EventDetail)
async def get_event(event_id: uuid.UUID, service: EventService = Depends(get_event_service)):
    try:
        return await service.get_event_detail(event_id)
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

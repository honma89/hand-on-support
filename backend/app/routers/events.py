import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ForbiddenError, NotFoundError
from app.db.session import get_db
from app.deps import CurrentUser, require_organizer_or_admin
from app.models.enums import EventStatus
from app.repositories.event_repository import EventRepository
from app.schemas.event import EventCreate, EventDetail, EventPublic, EventUpdate
from app.services.event_service import EventService

router = APIRouter(prefix="/events", tags=["events"])


def get_event_service(db: AsyncSession = Depends(get_db)) -> EventService:
    return EventService(EventRepository(db))


@router.get("", response_model=list[EventPublic])
async def list_events(
    status_filter: EventStatus | None = Query(default=None, alias="status"),
    category: str | None = None,
    dzongkhag: str | None = None,
    upcoming_only: bool = False,
    organizer_id: uuid.UUID | None = None,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    service: EventService = Depends(get_event_service),
):
    return await service.list_events(
        status=status_filter,
        category=category,
        dzongkhag=dzongkhag,
        upcoming_only=upcoming_only,
        organizer_id=organizer_id,
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

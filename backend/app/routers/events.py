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


def get_event_repository(db: AsyncSession = Depends(get_db)) -> EventRepository:
    return EventRepository(db)


@router.get("", response_model=list[EventPublic])
async def list_events(
    status_filter: EventStatus | None = Query(default=EventStatus.PUBLISHED, alias="status"),
    category: str | None = None,
    dzongkhag: str | None = None,
    upcoming_only: bool = True,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    event_repo: EventRepository = Depends(get_event_repository),
):
    service = EventService(event_repo)
    return await service.list_events(
        status=status_filter,
        category=category,
        dzongkhag=dzongkhag,
        upcoming_only=upcoming_only,
        offset=offset,
        limit=limit,
    )


@router.get("/{event_id}", response_model=EventDetail)
async def get_event(
    event_id: uuid.UUID,
    event_repo: EventRepository = Depends(get_event_repository),
):
    service = EventService(event_repo)
    try:
        return await service.get_detail(event_id)
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
    event_repo: EventRepository = Depends(get_event_repository),
):
    service = EventService(event_repo)
    event = await service.create(data, organizer=current_user)
    await db.commit()
    return event


@router.put(
    "/{event_id}",
    response_model=EventPublic,
    dependencies=[Depends(require_organizer_or_admin)],
)
async def update_event(
    event_id: uuid.UUID,
    data: EventUpdate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    event_repo: EventRepository = Depends(get_event_repository),
):
    service = EventService(event_repo)
    try:
        event = await service.update(event_id, data, actor=current_user)
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
    event_repo: EventRepository = Depends(get_event_repository),
):
    service = EventService(event_repo)
    try:
        await service.delete(event_id, actor=current_user)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    await db.commit()

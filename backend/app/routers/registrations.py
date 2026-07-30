import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError
from app.db.session import get_db
from app.deps import CurrentUser
from app.models.enums import RegistrationStatus
from app.repositories.event_repository import EventRepository
from app.repositories.notification_repository import NotificationRepository
from app.repositories.registration_repository import RegistrationRepository
from app.schemas.registration import RegistrationPublic, RegistrationWithEvent
from app.services.notification_service import NotificationService
from app.services.registration_service import RegistrationService

router = APIRouter(tags=["registrations"])


def get_registration_service(db: AsyncSession = Depends(get_db)) -> RegistrationService:
    return RegistrationService(
        RegistrationRepository(db),
        EventRepository(db),
        NotificationService(NotificationRepository(db)),
    )


@router.post(
    "/events/{event_id}/register",
    response_model=RegistrationPublic,
    status_code=status.HTTP_201_CREATED,
)
async def register_for_event(
    event_id: uuid.UUID,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    service: RegistrationService = Depends(get_registration_service),
):
    try:
        registration = await service.register_for_event(event_id, current_user)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)
    await db.commit()
    return registration


@router.delete(
    "/events/{event_id}/register",
    response_model=RegistrationPublic,
)
async def cancel_registration(
    event_id: uuid.UUID,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    service: RegistrationService = Depends(get_registration_service),
):
    try:
        registration = await service.cancel_registration(event_id, current_user)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    await db.commit()
    return registration


@router.get("/registrations/me", response_model=list[RegistrationWithEvent])
async def list_my_registrations(
    current_user: CurrentUser,
    service: RegistrationService = Depends(get_registration_service),
):
    return await service.list_my_registrations(current_user)


@router.get("/events/{event_id}/registrations", response_model=list[RegistrationPublic])
async def list_event_registrations(
    event_id: uuid.UUID,
    current_user: CurrentUser,
    status_filter: RegistrationStatus | None = None,
    service: RegistrationService = Depends(get_registration_service),
):
    try:
        return await service.list_event_registrations(event_id, current_user, status=status_filter)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)

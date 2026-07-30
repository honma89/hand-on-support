import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ForbiddenError, NotFoundError
from app.db.session import get_db
from app.deps import CurrentUser
from app.repositories.notification_repository import NotificationRepository
from app.schemas.notification import NotificationPublic, UnreadCountResponse
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["notifications"])


def get_notification_service(db: AsyncSession = Depends(get_db)) -> NotificationService:
    return NotificationService(NotificationRepository(db))


@router.get("", response_model=list[NotificationPublic])
async def list_my_notifications(
    current_user: CurrentUser,
    unread_only: bool = False,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    service: NotificationService = Depends(get_notification_service),
):
    return await service.list_for_user(current_user.id, unread_only, offset, limit)


@router.get("/unread-count", response_model=UnreadCountResponse)
async def get_unread_count(
    current_user: CurrentUser,
    service: NotificationService = Depends(get_notification_service),
):
    count = await service.count_unread(current_user.id)
    return UnreadCountResponse(unread_count=count)


@router.post("/{notification_id}/read", response_model=NotificationPublic)
async def mark_notification_read(
    notification_id: uuid.UUID,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    service: NotificationService = Depends(get_notification_service),
):
    try:
        notification = await service.mark_read(notification_id, current_user.id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    await db.commit()
    return notification


@router.post("/read-all", status_code=status.HTTP_204_NO_CONTENT)
async def mark_all_read(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    service: NotificationService = Depends(get_notification_service),
):
    await service.mark_all_read(current_user.id)
    await db.commit()

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ForbiddenError, NotFoundError
from app.db.session import get_db
from app.deps import CurrentUser
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.badge_repository import BadgeRepository
from app.repositories.event_repository import EventRepository
from app.repositories.notification_repository import NotificationRepository
from app.repositories.point_repository import PointRepository
from app.schemas.attendance import AttendanceMarkRequest, AttendancePublic, BulkAttendanceMarkRequest
from app.services.attendance_service import AttendanceService
from app.services.badge_service import BadgeService
from app.services.notification_service import NotificationService
from app.services.point_service import PointService

router = APIRouter(prefix="/events/{event_id}/attendance", tags=["attendance"])


def get_attendance_service(db: AsyncSession = Depends(get_db)) -> AttendanceService:
    attendance_repo = AttendanceRepository(db)
    point_repo = PointRepository(db)
    notification_service = NotificationService(NotificationRepository(db))
    return AttendanceService(
        attendance_repo,
        EventRepository(db),
        PointService(point_repo),
        BadgeService(BadgeRepository(db), attendance_repo, point_repo, notification_service),
        notification_service,
    )


@router.post("", response_model=AttendancePublic, status_code=status.HTTP_201_CREATED)
async def mark_attendance(
    event_id: uuid.UUID,
    record: AttendanceMarkRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    service: AttendanceService = Depends(get_attendance_service),
):
    try:
        attendance = await service.mark_attendance(event_id, record, current_user)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    await db.commit()
    return attendance


@router.post("/bulk", response_model=list[AttendancePublic], status_code=status.HTTP_201_CREATED)
async def mark_bulk_attendance(
    event_id: uuid.UUID,
    payload: BulkAttendanceMarkRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    service: AttendanceService = Depends(get_attendance_service),
):
    try:
        results = await service.mark_bulk(event_id, payload.records, current_user)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    await db.commit()
    return results


@router.get("", response_model=list[AttendancePublic])
async def list_event_attendance(
    event_id: uuid.UUID,
    current_user: CurrentUser,
    service: AttendanceService = Depends(get_attendance_service),
):
    try:
        return await service.list_for_event(event_id, current_user)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)

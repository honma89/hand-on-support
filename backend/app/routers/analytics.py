from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.deps import require_admin
from app.repositories.analytics_repository import AnalyticsRepository
from app.schemas.analytics import AttendanceRate, CategoryCount, DzongkhagPoints, MonthlyGrowth
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"], dependencies=[Depends(require_admin)])


def get_analytics_service(db: AsyncSession = Depends(get_db)) -> AnalyticsService:
    return AnalyticsService(AnalyticsRepository(db))


@router.get("/events-by-category", response_model=list[CategoryCount])
async def events_by_category(service: AnalyticsService = Depends(get_analytics_service)):
    return await service.get_events_by_category()


@router.get("/volunteer-growth", response_model=list[MonthlyGrowth])
async def volunteer_growth(service: AnalyticsService = Depends(get_analytics_service)):
    return await service.get_volunteer_growth()


@router.get("/points-by-dzongkhag", response_model=list[DzongkhagPoints])
async def points_by_dzongkhag(service: AnalyticsService = Depends(get_analytics_service)):
    return await service.get_points_by_dzongkhag()


@router.get("/attendance-rate", response_model=AttendanceRate)
async def attendance_rate(service: AnalyticsService = Depends(get_analytics_service)):
    return await service.get_attendance_rate()

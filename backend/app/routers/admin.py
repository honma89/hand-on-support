from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.deps import require_admin
from app.repositories.admin_repository import AdminRepository
from app.schemas.admin import DashboardStats
from app.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])


def get_admin_service(db: AsyncSession = Depends(get_db)) -> AdminService:
    return AdminService(AdminRepository(db))


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard(service: AdminService = Depends(get_admin_service)):
    return await service.get_dashboard_stats()

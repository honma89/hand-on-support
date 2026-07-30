from app.models.enums import EventStatus, UserRole
from app.repositories.admin_repository import AdminRepository
from app.schemas.admin import DashboardStats


class AdminService:
    def __init__(self, admin_repo: AdminRepository):
        self.admin_repo = admin_repo

    async def get_dashboard_stats(self) -> DashboardStats:
        return DashboardStats(
            total_users=await self.admin_repo.count_users_by_role(),
            total_volunteers=await self.admin_repo.count_users_by_role(UserRole.VOLUNTEER),
            total_organizers=await self.admin_repo.count_users_by_role(UserRole.ORGANIZER),
            total_events=await self.admin_repo.count_events(),
            published_events=await self.admin_repo.count_events(status=EventStatus.PUBLISHED),
            upcoming_events=await self.admin_repo.count_events(
                status=EventStatus.PUBLISHED, upcoming_only=True
            ),
            total_registrations=await self.admin_repo.count_registrations(),
            total_attendance_present=await self.admin_repo.count_attendance_present(),
            total_points_awarded=await self.admin_repo.sum_points_awarded(),
            total_badges_awarded=await self.admin_repo.count_badges_awarded(),
        )

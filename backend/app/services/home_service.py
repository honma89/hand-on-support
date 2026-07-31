from app.models.enums import EventStatus, UserRole
from app.repositories.admin_repository import AdminRepository
from app.repositories.announcement_repository import AnnouncementRepository
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.event_repository import EventRepository
from app.schemas.home import HomeResponse, HomeStats
from app.services.leaderboard_service import LeaderboardScope, LeaderboardService

UPCOMING_EVENTS_LIMIT = 5
ANNOUNCEMENTS_LIMIT = 5
LEADERBOARD_LIMIT = 5


class HomeService:
    """Assembles the public landing-page bundle out of repositories that
    already exist elsewhere (events, announcements, leaderboard, admin
    stats) - this is a read-model, not a new source of truth."""

    def __init__(
        self,
        event_repo: EventRepository,
        announcement_repo: AnnouncementRepository,
        admin_repo: AdminRepository,
        attendance_repo: AttendanceRepository,
        leaderboard_service: LeaderboardService,
    ):
        self.event_repo = event_repo
        self.announcement_repo = announcement_repo
        self.admin_repo = admin_repo
        self.attendance_repo = attendance_repo
        self.leaderboard_service = leaderboard_service

    async def get_home(self) -> HomeResponse:
        upcoming_events = await self.event_repo.list_filtered(
            status=EventStatus.PUBLISHED,
            upcoming_only=True,
            limit=UPCOMING_EVENTS_LIMIT,
        )
        announcements = (await self.announcement_repo.list_all())[:ANNOUNCEMENTS_LIMIT]
        leaderboard = await self.leaderboard_service.get_leaderboard(
            scope=LeaderboardScope.ALL_TIME, limit=LEADERBOARD_LIMIT
        )

        stats = HomeStats(
            total_volunteers=await self.admin_repo.count_users_by_role(UserRole.VOLUNTEER),
            total_events_completed=await self.admin_repo.count_events(status=EventStatus.COMPLETED),
            total_hours_logged=await self.attendance_repo.sum_hours_all(),
            total_points_awarded=await self.admin_repo.sum_points_awarded(),
        )

        return HomeResponse(
            upcoming_events=upcoming_events,
            announcements=announcements,
            leaderboard=leaderboard,
            stats=stats,
        )

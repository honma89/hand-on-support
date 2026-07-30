import uuid

from app.models.badge import Badge, UserBadge
from app.models.enums import BadgeCriteriaType, NotificationType
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.badge_repository import BadgeRepository
from app.repositories.point_repository import PointRepository
from app.services.notification_service import NotificationService


class BadgeService:
    def __init__(
        self,
        badge_repo: BadgeRepository,
        attendance_repo: AttendanceRepository,
        point_repo: PointRepository,
        notification_service: NotificationService | None = None,
    ):
        self.badge_repo = badge_repo
        self.attendance_repo = attendance_repo
        self.point_repo = point_repo
        self.notification_service = notification_service

    async def list_all(self) -> list[Badge]:
        return await self.badge_repo.list_all()

    async def list_for_user(self, user_id: uuid.UUID) -> list[UserBadge]:
        return await self.badge_repo.list_for_user(user_id)

    async def evaluate_and_award(self, user_id: uuid.UUID) -> list[UserBadge]:
        """
        Checks every badge's criteria against the user's current stats and
        awards any newly-earned ones. Called after attendance is marked
        PRESENT (see AttendanceService), which is the only event that can
        move either criteria metric.
        """
        all_badges = await self.badge_repo.list_all()
        earned_ids = await self.badge_repo.list_earned_badge_ids(user_id)

        events_attended: int | None = None
        points_earned: int | None = None
        newly_awarded: list[UserBadge] = []

        for badge in all_badges:
            if badge.id in earned_ids:
                continue

            if badge.criteria_type == BadgeCriteriaType.EVENTS_ATTENDED:
                if events_attended is None:
                    events_attended = await self.attendance_repo.count_present_for_user(user_id)
                current_value = events_attended
            else:  # POINTS_EARNED
                if points_earned is None:
                    points_earned = await self.point_repo.get_balance(user_id)
                current_value = points_earned

            if current_value >= badge.criteria_value:
                user_badge = await self.badge_repo.award(user_id, badge.id)
                user_badge.badge = badge
                newly_awarded.append(user_badge)

                if self.notification_service:
                    await self.notification_service.notify(
                        user_id=user_id,
                        type=NotificationType.BADGE_EARNED,
                        title=f"Badge earned: {badge.name}",
                        message=f'You earned the "{badge.name}" badge — {badge.description}',
                        related_entity_id=badge.id,
                    )

        return newly_awarded

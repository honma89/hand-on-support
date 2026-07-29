import uuid

from app.models.badge import Badge, UserBadge
from app.models.enums import BadgeCriteriaType, NotificationType
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.badge_repository import BadgeRepository
from app.repositories.point_repository import PointRepository
from app.schemas.badge import BadgeCreate
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

    async def create_badge(self, data: BadgeCreate) -> Badge:
        badge = Badge(**data.model_dump())
        return await self.badge_repo.create(badge)

    async def list_badges(self) -> list[Badge]:
        return await self.badge_repo.list_all()

    async def list_user_badges(self, user_id: uuid.UUID) -> list[UserBadge]:
        return await self.badge_repo.list_for_user(user_id)

    async def evaluate_and_award(self, user_id: uuid.UUID) -> list[UserBadge]:
        """
        Checks every badge's criteria against the user's current stats and
        awards any newly-qualified badges. Safe to call as often as needed
        (e.g. after every attendance mark) — already-earned badges are
        skipped via the unique (user_id, badge_id) constraint check.
        """
        all_badges = await self.badge_repo.list_all()
        already_earned = await self.badge_repo.list_earned_badge_ids(user_id)

        events_attended = await self.attendance_repo.count_present_for_user(user_id)
        points_balance = await self.point_repo.get_balance(user_id)

        newly_awarded: list[UserBadge] = []
        for badge in all_badges:
            if badge.id in already_earned:
                continue

            qualifies = (
                badge.criteria_type == BadgeCriteriaType.EVENTS_ATTENDED
                and events_attended >= badge.criteria_value
            ) or (
                badge.criteria_type == BadgeCriteriaType.POINTS_EARNED
                and points_balance >= badge.criteria_value
            )

            if qualifies:
                user_badge = await self.badge_repo.award(user_id, badge.id)
                newly_awarded.append(user_badge)
                if self.notification_service:
                    await self.notification_service.notify(
                        user_id=user_id,
                        type=NotificationType.BADGE_EARNED,
                        title=f"New badge earned: {badge.name}",
                        message=badge.description,
                        related_entity_id=badge.id,
                    )

        return newly_awarded

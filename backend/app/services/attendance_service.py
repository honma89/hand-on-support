import uuid

from app.core.exceptions import ForbiddenError, NotFoundError
from app.models.attendance import Attendance
from app.models.enums import AttendanceStatus, NotificationType, PointTransactionType, UserRole
from app.models.user import User
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.event_repository import EventRepository
from app.schemas.attendance import AttendanceMarkRequest
from app.services.badge_service import BadgeService
from app.services.notification_service import NotificationService
from app.services.point_service import PointService


class AttendanceService:
    def __init__(
        self,
        attendance_repo: AttendanceRepository,
        event_repo: EventRepository,
        point_service: PointService,
        badge_service: BadgeService | None = None,
        notification_service: NotificationService | None = None,
    ):
        self.attendance_repo = attendance_repo
        self.event_repo = event_repo
        self.point_service = point_service
        self.badge_service = badge_service
        self.notification_service = notification_service

    def _assert_can_mark(self, event_organizer_id: uuid.UUID, actor: User) -> None:
        if actor.role == UserRole.ADMIN:
            return
        if actor.role == UserRole.ORGANIZER and event_organizer_id == actor.id:
            return
        raise ForbiddenError("You do not have permission to mark attendance for this event.")

    async def mark_attendance(
        self, event_id: uuid.UUID, record: AttendanceMarkRequest, actor: User
    ) -> Attendance:
        event = await self.event_repo.get_by_id(event_id)
        if not event:
            raise NotFoundError("Event not found.")
        self._assert_can_mark(event.organizer_id, actor)

        existing = await self.attendance_repo.get_by_event_and_user(event_id, record.user_id)
        if existing:
            existing.status = record.status
            existing.marked_by_id = actor.id
            attendance = existing
        else:
            attendance = Attendance(
                event_id=event_id,
                user_id=record.user_id,
                status=record.status,
                marked_by_id=actor.id,
            )
            attendance = await self.attendance_repo.create(attendance)

        # Award points exactly once, the first time a volunteer is marked
        # PRESENT for this event -- points_awarded is the idempotency guard.
        if record.status == AttendanceStatus.PRESENT and not attendance.points_awarded:
            await self.point_service.award_points(
                user_id=attendance.user_id,
                amount=event.points_reward,
                description=f'Attended "{event.title}"',
                event_id=event.id,
                transaction_type=PointTransactionType.EARNED,
                created_by_id=actor.id,
            )
            attendance.points_awarded = True
            if self.notification_service:
                await self.notification_service.notify(
                    user_id=attendance.user_id,
                    type=NotificationType.POINTS_AWARDED,
                    title=f"+{event.points_reward} points earned",
                    message=f'You earned {event.points_reward} points for attending "{event.title}".',
                    related_entity_id=event.id,
                )
            if self.badge_service:
                await self.badge_service.evaluate_and_award(attendance.user_id)

        return await self.attendance_repo.save(attendance)

    async def mark_bulk(
        self, event_id: uuid.UUID, records: list[AttendanceMarkRequest], actor: User
    ) -> list[Attendance]:
        return [await self.mark_attendance(event_id, record, actor) for record in records]

    async def list_for_event(self, event_id: uuid.UUID, actor: User) -> list[Attendance]:
        event = await self.event_repo.get_by_id(event_id)
        if not event:
            raise NotFoundError("Event not found.")
        self._assert_can_mark(event.organizer_id, actor)
        return await self.attendance_repo.list_for_event(event_id)

    async def list_for_user(self, user_id: uuid.UUID) -> list[Attendance]:
        return await self.attendance_repo.list_for_user(user_id)

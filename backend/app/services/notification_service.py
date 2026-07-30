import uuid

from app.core.exceptions import ForbiddenError, NotFoundError
from app.models.enums import NotificationType
from app.models.notification import Notification
from app.repositories.notification_repository import NotificationRepository


class NotificationService:
    def __init__(self, notification_repo: NotificationRepository):
        self.notification_repo = notification_repo

    async def notify(
        self,
        user_id: uuid.UUID,
        type: NotificationType,
        title: str,
        message: str,
        related_entity_id: uuid.UUID | None = None,
    ) -> Notification:
        """
        Single write-path for creating notifications. Other services (event
        registration, attendance, point bank, badges) call this rather than
        constructing Notification rows themselves.
        """
        notification = Notification(
            user_id=user_id,
            type=type,
            title=title,
            message=message,
            related_entity_id=related_entity_id,
        )
        return await self.notification_repo.create(notification)

    async def list_for_user(self, user_id: uuid.UUID, unread_only: bool, offset: int, limit: int):
        return await self.notification_repo.list_for_user(
            user_id, unread_only=unread_only, offset=offset, limit=limit
        )

    async def count_unread(self, user_id: uuid.UUID) -> int:
        return await self.notification_repo.count_unread(user_id)

    async def mark_read(self, notification_id: uuid.UUID, actor_id: uuid.UUID) -> Notification:
        notification = await self.notification_repo.get_by_id(notification_id)
        if not notification:
            raise NotFoundError("Notification not found.")
        if notification.user_id != actor_id:
            raise ForbiddenError("You cannot modify another user's notification.")
        notification.is_read = True
        return await self.notification_repo.save(notification)

    async def mark_all_read(self, user_id: uuid.UUID) -> None:
        await self.notification_repo.mark_all_read(user_id)

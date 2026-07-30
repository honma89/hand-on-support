import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification


class NotificationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, notification: Notification) -> Notification:
        self.db.add(notification)
        await self.db.flush()
        await self.db.refresh(notification)
        return notification

    async def get_by_id(self, notification_id: uuid.UUID) -> Notification | None:
        return await self.db.get(Notification, notification_id)

    async def save(self, notification: Notification) -> Notification:
        await self.db.flush()
        await self.db.refresh(notification)
        return notification

    async def list_for_user(
        self, user_id: uuid.UUID, unread_only: bool = False, offset: int = 0, limit: int = 50
    ) -> list[Notification]:
        query = select(Notification).where(Notification.user_id == user_id)
        if unread_only:
            query = query.where(Notification.is_read.is_(False))
        query = query.order_by(Notification.created_at.desc()).offset(offset).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count_unread(self, user_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(func.count())
            .select_from(Notification)
            .where(Notification.user_id == user_id, Notification.is_read.is_(False))
        )
        return int(result.scalar_one())

    async def mark_all_read(self, user_id: uuid.UUID) -> None:
        notifications = await self.list_for_user(user_id, unread_only=True, limit=10_000)
        for n in notifications:
            n.is_read = True
        await self.db.flush()

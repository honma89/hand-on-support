import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.badge import Badge, UserBadge


class BadgeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, badge: Badge) -> Badge:
        self.db.add(badge)
        await self.db.flush()
        await self.db.refresh(badge)
        return badge

    async def list_all(self) -> list[Badge]:
        result = await self.db.execute(select(Badge).order_by(Badge.criteria_value.asc()))
        return list(result.scalars().all())

    async def list_earned_badge_ids(self, user_id: uuid.UUID) -> set[uuid.UUID]:
        result = await self.db.execute(select(UserBadge.badge_id).where(UserBadge.user_id == user_id))
        return set(result.scalars().all())

    async def award(self, user_id: uuid.UUID, badge_id: uuid.UUID) -> UserBadge:
        user_badge = UserBadge(user_id=user_id, badge_id=badge_id)
        self.db.add(user_badge)
        await self.db.flush()
        await self.db.refresh(user_badge)
        return user_badge

    async def list_for_user(self, user_id: uuid.UUID) -> list[UserBadge]:
        result = await self.db.execute(
            select(UserBadge)
            .where(UserBadge.user_id == user_id)
            .options(selectinload(UserBadge.badge))
            .order_by(UserBadge.awarded_at.desc())
        )
        return list(result.scalars().all())

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.point_transaction import PointTransaction


class PointRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, transaction: PointTransaction) -> PointTransaction:
        self.db.add(transaction)
        await self.db.flush()
        await self.db.refresh(transaction)
        return transaction

    async def get_balance(self, user_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(func.coalesce(func.sum(PointTransaction.amount), 0)).where(
                PointTransaction.user_id == user_id
            )
        )
        return int(result.scalar_one())

    async def list_for_user(
        self, user_id: uuid.UUID, offset: int = 0, limit: int = 50
    ) -> list[PointTransaction]:
        result = await self.db.execute(
            select(PointTransaction)
            .where(PointTransaction.user_id == user_id)
            .order_by(PointTransaction.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_leaderboard(
        self, since: object | None = None, limit: int = 50
    ) -> list[tuple[uuid.UUID, int]]:
        """Returns [(user_id, total_points), ...] sorted descending, optionally
        restricted to transactions created since a given datetime (for
        monthly/weekly leaderboards)."""
        query = select(
            PointTransaction.user_id, func.sum(PointTransaction.amount).label("total")
        ).group_by(PointTransaction.user_id)
        if since is not None:
            query = query.where(PointTransaction.created_at >= since)
        query = query.order_by(func.sum(PointTransaction.amount).desc()).limit(limit)
        result = await self.db.execute(query)
        return [(row.user_id, int(row.total)) for row in result.all()]

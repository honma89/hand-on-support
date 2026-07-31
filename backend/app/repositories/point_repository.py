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

    async def get_user_rank(self, user_id: uuid.UUID, since: object | None = None) -> int | None:
        """1-based leaderboard rank for a single user (None if they have no
        transactions at all yet). Counts how many other users out-earn them
        rather than materializing the full ranking, so it stays cheap
        regardless of how many volunteers are registered."""
        totals_query = select(
            PointTransaction.user_id.label("user_id"),
            func.sum(PointTransaction.amount).label("total"),
        ).group_by(PointTransaction.user_id)
        if since is not None:
            totals_query = totals_query.where(PointTransaction.created_at >= since)
        totals = totals_query.subquery()

        my_total = (
            await self.db.execute(select(totals.c.total).where(totals.c.user_id == user_id))
        ).scalar_one_or_none()
        if my_total is None:
            return None

        higher_count = (
            await self.db.execute(
                select(func.count()).select_from(totals).where(totals.c.total > my_total)
            )
        ).scalar_one()
        return int(higher_count) + 1

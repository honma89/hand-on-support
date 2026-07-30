import uuid

from app.core.exceptions import ValidationError
from app.models.enums import PointTransactionType
from app.models.point_transaction import PointTransaction
from app.repositories.point_repository import PointRepository


class PointService:
    """
    Append-only point ledger. Balances are always derived by summing
    transactions (see PointTransaction docstring) -- this service never
    writes a cached balance anywhere.
    """

    def __init__(self, point_repo: PointRepository):
        self.point_repo = point_repo

    async def get_balance(self, user_id: uuid.UUID) -> int:
        return await self.point_repo.get_balance(user_id)

    async def get_history(
        self, user_id: uuid.UUID, offset: int = 0, limit: int = 50
    ) -> list[PointTransaction]:
        return await self.point_repo.list_for_user(user_id, offset=offset, limit=limit)

    async def award_points(
        self,
        user_id: uuid.UUID,
        amount: int,
        description: str,
        event_id: uuid.UUID | None = None,
        transaction_type: PointTransactionType = PointTransactionType.EARNED,
        created_by_id: uuid.UUID | None = None,
    ) -> PointTransaction:
        transaction = PointTransaction(
            user_id=user_id,
            event_id=event_id,
            amount=amount,
            type=transaction_type,
            description=description,
            created_by_id=created_by_id,
        )
        return await self.point_repo.create(transaction)

    async def redeem_points(
        self, user_id: uuid.UUID, amount: int, description: str
    ) -> PointTransaction:
        balance = await self.point_repo.get_balance(user_id)
        if amount > balance:
            raise ValidationError("Insufficient point balance for this redemption.")

        return await self.point_repo.create(
            PointTransaction(
                user_id=user_id,
                amount=-amount,
                type=PointTransactionType.REDEEMED,
                description=description,
                created_by_id=user_id,
            )
        )

    async def adjust_points(
        self, user_id: uuid.UUID, amount: int, description: str, admin_id: uuid.UUID
    ) -> PointTransaction:
        if amount == 0:
            raise ValidationError("Adjustment amount cannot be zero.")

        return await self.point_repo.create(
            PointTransaction(
                user_id=user_id,
                amount=amount,
                type=PointTransactionType.ADJUSTMENT,
                description=description,
                created_by_id=admin_id,
            )
        )

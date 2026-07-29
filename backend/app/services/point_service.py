import uuid

from app.core.exceptions import ValidationError
from app.models.enums import PointTransactionType
from app.models.point_transaction import PointTransaction
from app.repositories.point_repository import PointRepository


class PointService:
    """
    Single write-path for the Point Bank ledger. Every other module
    (Attendance, Badges, Admin) goes through this service rather than
    inserting PointTransaction rows directly, so balance rules stay
    consistent in one place.
    """

    def __init__(self, point_repo: PointRepository):
        self.point_repo = point_repo

    async def award_points(
        self,
        user_id: uuid.UUID,
        amount: int,
        description: str,
        event_id: uuid.UUID | None = None,
        transaction_type: PointTransactionType = PointTransactionType.EARNED,
        created_by_id: uuid.UUID | None = None,
    ) -> PointTransaction:
        if amount == 0:
            raise ValidationError("Point amount cannot be zero.")
        transaction = PointTransaction(
            user_id=user_id,
            event_id=event_id,
            amount=amount,
            type=transaction_type,
            description=description,
            created_by_id=created_by_id,
        )
        return await self.point_repo.create(transaction)

    async def redeem_points(self, user_id: uuid.UUID, amount: int, description: str) -> PointTransaction:
        if amount <= 0:
            raise ValidationError("Redemption amount must be positive.")
        balance = await self.point_repo.get_balance(user_id)
        if balance < amount:
            raise ValidationError("Insufficient point balance for this redemption.")
        transaction = PointTransaction(
            user_id=user_id,
            amount=-amount,
            type=PointTransactionType.REDEEMED,
            description=description,
        )
        return await self.point_repo.create(transaction)

    async def adjust_points(
        self, user_id: uuid.UUID, amount: int, description: str, admin_id: uuid.UUID
    ) -> PointTransaction:
        return await self.award_points(
            user_id=user_id,
            amount=amount,
            description=description,
            transaction_type=PointTransactionType.ADJUSTMENT,
            created_by_id=admin_id,
        )

    async def get_balance(self, user_id: uuid.UUID) -> int:
        return await self.point_repo.get_balance(user_id)

    async def get_history(self, user_id: uuid.UUID, offset: int = 0, limit: int = 50) -> list[PointTransaction]:
        return await self.point_repo.list_for_user(user_id, offset=offset, limit=limit)

import uuid

from app.core.exceptions import NotFoundError
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import AdminUserUpdate, UserUpdate


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_by_id_or_raise(self, user_id: uuid.UUID) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found.")
        return user

    async def update_own_profile(self, user: User, data: UserUpdate) -> User:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        return await self.user_repo.save(user)

    async def admin_update_user(self, user_id: uuid.UUID, data: AdminUserUpdate) -> User:
        user = await self.get_by_id_or_raise(user_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        return await self.user_repo.save(user)

    async def list_users(self, offset: int, limit: int) -> list[User]:
        return await self.user_repo.list_all(offset=offset, limit=limit)

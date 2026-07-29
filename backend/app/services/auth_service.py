from app.core.exceptions import ConflictError, UnauthorizedError
from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.models.enums import UserRole
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register(self, data: RegisterRequest) -> User:
        existing = await self.user_repo.get_by_email(data.email)
        if existing:
            raise ConflictError("An account with this email already exists.")

        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
            phone_number=data.phone_number,
            role=UserRole.VOLUNTEER,
        )
        return await self.user_repo.create(user)

    async def authenticate(self, email: str, password: str) -> User:
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password.")
        if not user.is_active:
            raise UnauthorizedError("This account has been deactivated.")
        return user

    @staticmethod
    def issue_tokens(user: User) -> tuple[str, str]:
        """Returns (access_token, refresh_token)."""
        access_token = create_access_token(user_id=str(user.id), role=user.role.value)
        refresh_token = create_refresh_token(user_id=str(user.id))
        return access_token, refresh_token

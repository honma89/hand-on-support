import uuid
from typing import Annotated

from fastapi import Cookie, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import TokenType, decode_token
from app.db.session import get_db
from app.models.enums import UserRole
from app.models.user import User
from app.repositories.user_repository import UserRepository


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


async def get_current_user(
    access_token_cookie: str | None = Cookie(default=None, alias="access_token"),
    authorization: str | None = Header(default=None),
    user_repo: UserRepository = Depends(get_user_repository),
) -> User:
    """
    Resolves the current user from either the HttpOnly access-token cookie
    (normal browser flow) or a Bearer header (useful for API clients/tests).
    Cookie takes precedence since it's what the frontend actually uses.
    """
    token = access_token_cookie
    if not token and authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:]

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception

    payload = decode_token(token)
    if not payload or payload.get("type") != TokenType.ACCESS.value:
        raise credentials_exception

    user_id = payload.get("sub")
    if not user_id:
        raise credentials_exception

    try:
        user = await user_repo.get_by_id(uuid.UUID(user_id))
    except ValueError:
        raise credentials_exception

    if not user or not user.is_active:
        raise credentials_exception

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


async def get_current_user_optional(
    access_token_cookie: str | None = Cookie(default=None, alias="access_token"),
    authorization: str | None = Header(default=None),
    user_repo: UserRepository = Depends(get_user_repository),
) -> User | None:
    """
    Like get_current_user, but returns None instead of raising when no
    valid session is present. For endpoints that are public but need to
    behave differently for logged-in users (e.g. an events list that
    shows drafts to their organizer but not to anonymous visitors).
    """
    token = access_token_cookie
    if not token and authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:]
    if not token:
        return None

    payload = decode_token(token)
    if not payload or payload.get("type") != TokenType.ACCESS.value:
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None

    try:
        user = await user_repo.get_by_id(uuid.UUID(user_id))
    except ValueError:
        return None

    if not user or not user.is_active:
        return None

    return user


CurrentUserOptional = Annotated[User | None, Depends(get_current_user_optional)]


def require_roles(*allowed_roles: UserRole):
    """
    Dependency factory for role-based authorization, e.g.:
        @router.post(..., dependencies=[Depends(require_roles(UserRole.ADMIN))])
    """

    async def _check(current_user: CurrentUser) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )
        return current_user

    return _check


require_admin = require_roles(UserRole.ADMIN)
require_organizer_or_admin = require_roles(UserRole.ORGANIZER, UserRole.ADMIN)

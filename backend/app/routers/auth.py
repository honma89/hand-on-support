from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.exceptions import ConflictError, UnauthorizedError
from app.core.security import TokenType, create_access_token, decode_token
from app.db.session import get_db
from app.deps import CurrentUser, get_user_repository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()

ACCESS_COOKIE_NAME = "access_token"
REFRESH_COOKIE_NAME = "refresh_token"


def _set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    is_prod = settings.APP_ENV == "production"
    response.set_cookie(
        key=ACCESS_COOKIE_NAME,
        value=access_token,
        httponly=True,
        secure=is_prod,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=is_prod,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        # Scoped to the refresh endpoint only — the browser never needs to
        # send this cookie anywhere else, minimizing exposure.
        path="/api/v1/auth",
    )


def _clear_auth_cookies(response: Response) -> None:
    response.delete_cookie(ACCESS_COOKIE_NAME, path="/")
    response.delete_cookie(REFRESH_COOKIE_NAME, path="/api/v1/auth")


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
    user_repo: UserRepository = Depends(get_user_repository),
):
    service = AuthService(user_repo)
    try:
        user = await service.register(data)
        await db.commit()
    except ConflictError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)

    access_token, refresh_token = service.issue_tokens(user)
    _set_auth_cookies(response, access_token, refresh_token)
    return TokenResponse(access_token=access_token, user=UserPublic.model_validate(user))


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    response: Response,
    user_repo: UserRepository = Depends(get_user_repository),
):
    service = AuthService(user_repo)
    try:
        user = await service.authenticate(data.email, data.password)
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message)

    access_token, refresh_token = service.issue_tokens(user)
    _set_auth_cookies(response, access_token, refresh_token)
    return TokenResponse(access_token=access_token, user=UserPublic.model_validate(user))


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    response: Response,
    refresh_token: str | None = Cookie(default=None, alias=REFRESH_COOKIE_NAME),
    user_repo: UserRepository = Depends(get_user_repository),
):
    """
    Mints a new access token (and rotates the refresh token) from a valid
    refresh cookie. This is what lets the frontend keep a user logged in
    silently after the short-lived access token expires.
    """
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token."
    )

    if not refresh_token:
        raise unauthorized

    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != TokenType.REFRESH.value:
        raise unauthorized

    user_id = payload.get("sub")
    if not user_id:
        raise unauthorized

    import uuid as _uuid

    try:
        user = await user_repo.get_by_id(_uuid.UUID(user_id))
    except ValueError:
        raise unauthorized

    if not user or not user.is_active:
        raise unauthorized

    service = AuthService(user_repo)
    access_token, new_refresh_token = service.issue_tokens(user)
    _set_auth_cookies(response, access_token, new_refresh_token)
    return TokenResponse(access_token=access_token, user=UserPublic.model_validate(user))


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    _clear_auth_cookies(response)


@router.get("/me", response_model=UserPublic)
async def get_me(current_user: CurrentUser):
    return current_user

from pydantic import BaseModel, EmailStr, Field

from app.schemas.user import UserPublic


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=150)
    phone_number: str | None = Field(default=None, max_length=20)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """
    Access token is returned in the body (frontend keeps it in memory/React
    Query cache); refresh token is NEVER returned in the body — it's set
    as an HttpOnly cookie only, so client-side JS can never read it.
    """

    access_token: str
    token_type: str = "bearer"
    user: UserPublic


class RefreshRequest(BaseModel):
    """
    Present for completeness/testing via API docs. In normal browser flow
    the refresh token is read from the HttpOnly cookie, not the body.
    """

    refresh_token: str | None = None

import uuid

from pydantic import BaseModel


class LeaderboardEntry(BaseModel):
    rank: int
    user_id: uuid.UUID
    full_name: str
    avatar_url: str | None
    dzongkhag: str | None
    total_points: int

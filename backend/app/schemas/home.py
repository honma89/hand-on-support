from pydantic import BaseModel

from app.schemas.announcement import AnnouncementPublic
from app.schemas.event import EventPublic
from app.schemas.leaderboard import LeaderboardEntry


class HomeStats(BaseModel):
    total_volunteers: int
    total_events_completed: int
    total_hours_logged: float
    total_points_awarded: int


class HomeResponse(BaseModel):
    """Bundle for the public landing page: everything the homepage needs
    in a single round trip instead of four separate calls."""

    upcoming_events: list[EventPublic]
    announcements: list[AnnouncementPublic]
    leaderboard: list[LeaderboardEntry]
    stats: HomeStats

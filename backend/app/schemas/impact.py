from pydantic import BaseModel


class MyImpact(BaseModel):
    """One-call summary of a volunteer's own activity - powers a
    'my impact' card on their profile/dashboard."""

    events_attended: int
    hours_volunteered: float
    total_points: int
    badges_earned: int
    leaderboard_rank: int | None

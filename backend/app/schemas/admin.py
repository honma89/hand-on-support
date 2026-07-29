from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_users: int
    total_volunteers: int
    total_organizers: int
    total_events: int
    published_events: int
    upcoming_events: int
    total_registrations: int
    total_attendance_present: int
    total_points_awarded: int
    total_badges_awarded: int

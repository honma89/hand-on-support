import uuid

from pydantic import BaseModel

from app.models.enums import UserRole


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


class RoleAssign(BaseModel):
    user_id: uuid.UUID
    role: UserRole

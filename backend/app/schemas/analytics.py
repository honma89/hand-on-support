from datetime import datetime

from pydantic import BaseModel


class CategoryCount(BaseModel):
    category: str
    count: int


class MonthlyGrowth(BaseModel):
    month: datetime
    new_volunteers: int


class DzongkhagPoints(BaseModel):
    dzongkhag: str
    total_points: int


class AttendanceRate(BaseModel):
    total_registrations: int
    total_present: int
    total_absent: int
    attendance_rate_percent: float

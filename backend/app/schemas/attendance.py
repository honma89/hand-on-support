import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import AttendanceStatus


class AttendanceMarkRequest(BaseModel):
    user_id: uuid.UUID
    status: AttendanceStatus


class BulkAttendanceMarkRequest(BaseModel):
    records: list[AttendanceMarkRequest]


class AttendancePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    event_id: uuid.UUID
    user_id: uuid.UUID
    status: AttendanceStatus
    marked_at: datetime
    points_awarded: bool

from enum import StrEnum


class UserRole(StrEnum):
    VOLUNTEER = "volunteer"
    ORGANIZER = "organizer"
    ADMIN = "admin"


class EventStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class RegistrationStatus(StrEnum):
    REGISTERED = "registered"
    WAITLISTED = "waitlisted"
    CANCELLED = "cancelled"


class AttendanceStatus(StrEnum):
    PRESENT = "present"
    ABSENT = "absent"


class PointTransactionType(StrEnum):
    EARNED = "earned"          # awarded for attendance
    REDEEMED = "redeemed"      # spent by the volunteer
    ADJUSTMENT = "adjustment"  # manual admin correction (can be negative)
    BONUS = "bonus"            # ad-hoc admin bonus (e.g. badge milestone)


class BadgeCriteriaType(StrEnum):
    EVENTS_ATTENDED = "events_attended"  # count of PRESENT attendance records
    POINTS_EARNED = "points_earned"      # lifetime point balance threshold


class NotificationType(StrEnum):
    EVENT_REGISTRATION = "event_registration"
    EVENT_REMINDER = "event_reminder"
    EVENT_CANCELLED = "event_cancelled"
    ATTENDANCE_MARKED = "attendance_marked"
    POINTS_AWARDED = "points_awarded"
    BADGE_EARNED = "badge_earned"
    GENERAL = "general"

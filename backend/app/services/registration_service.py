import uuid

from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError
from app.models.enums import EventStatus, NotificationType, RegistrationStatus, UserRole
from app.models.event_registration import EventRegistration
from app.models.user import User
from app.repositories.event_repository import EventRepository
from app.repositories.registration_repository import RegistrationRepository
from app.services.notification_service import NotificationService


class RegistrationService:
    def __init__(
        self,
        registration_repo: RegistrationRepository,
        event_repo: EventRepository,
        notification_service: NotificationService | None = None,
    ):
        self.registration_repo = registration_repo
        self.event_repo = event_repo
        self.notification_service = notification_service

    async def register_for_event(self, event_id: uuid.UUID, user: User) -> EventRegistration:
        event = await self.event_repo.get_by_id(event_id)
        if not event:
            raise NotFoundError("Event not found.")
        if event.status != EventStatus.PUBLISHED:
            raise ConflictError("This event is not open for registration.")

        existing = await self.registration_repo.get_by_event_and_user(event_id, user.id)
        if existing and existing.status != RegistrationStatus.CANCELLED:
            raise ConflictError("You are already registered for this event.")

        active_count = await self.event_repo.count_active_registrations(event_id)
        is_full = event.capacity is not None and active_count >= event.capacity
        new_status = RegistrationStatus.WAITLISTED if is_full else RegistrationStatus.REGISTERED

        if existing:
            # Re-registering after a previous cancellation — reuse the row.
            existing.status = new_status
            registration = await self.registration_repo.save(existing)
        else:
            registration = EventRegistration(event_id=event_id, user_id=user.id, status=new_status)
            registration = await self.registration_repo.create(registration)

        if self.notification_service:
            if new_status == RegistrationStatus.REGISTERED:
                await self.notification_service.notify(
                    user_id=user.id,
                    type=NotificationType.EVENT_REGISTRATION,
                    title="Registration confirmed",
                    message=f'You are registered for "{event.title}".',
                    related_entity_id=event.id,
                )
            else:
                await self.notification_service.notify(
                    user_id=user.id,
                    type=NotificationType.EVENT_REGISTRATION,
                    title="Added to waitlist",
                    message=f'"{event.title}" is full — you have been waitlisted and will be '
                    "notified automatically if a spot opens up.",
                    related_entity_id=event.id,
                )

        return registration

    async def cancel_registration(self, event_id: uuid.UUID, user: User) -> EventRegistration:
        registration = await self.registration_repo.get_by_event_and_user(event_id, user.id)
        if not registration or registration.status == RegistrationStatus.CANCELLED:
            raise NotFoundError("Active registration not found.")

        was_registered = registration.status == RegistrationStatus.REGISTERED
        registration.status = RegistrationStatus.CANCELLED
        await self.registration_repo.save(registration)

        # Promote the longest-waiting waitlisted volunteer into the freed slot.
        if was_registered:
            next_in_line = await self.registration_repo.get_earliest_waitlisted(event_id)
            if next_in_line:
                next_in_line.status = RegistrationStatus.REGISTERED
                await self.registration_repo.save(next_in_line)
                if self.notification_service:
                    event = await self.event_repo.get_by_id(event_id)
                    await self.notification_service.notify(
                        user_id=next_in_line.user_id,
                        type=NotificationType.EVENT_REGISTRATION,
                        title="You're off the waitlist!",
                        message=f'A spot opened up in "{event.title}" and you have been registered.',
                        related_entity_id=event_id,
                    )

        return registration

    async def list_my_registrations(self, user: User) -> list[EventRegistration]:
        return await self.registration_repo.list_for_user(user.id)

    async def list_event_registrations(
        self, event_id: uuid.UUID, actor: User, status: RegistrationStatus | None = None
    ) -> list[EventRegistration]:
        event = await self.event_repo.get_by_id(event_id)
        if not event:
            raise NotFoundError("Event not found.")
        if actor.role != UserRole.ADMIN and event.organizer_id != actor.id:
            raise ForbiddenError("You do not have permission to view these registrations.")
        return await self.registration_repo.list_for_event(event_id, status=status)

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.event import Event
from app.models.event_registration import EventRegistration, RegistrationStatus
from app.schemas.event import EventCreate, EventUpdate


def create_event(db: Session, data: EventCreate, created_by):
    event = Event(
        title=data.title,
        description=data.description,
        event_date=data.event_date,
        department_id=data.department_id,
        location_id=data.location_id,
        max_volunteers=data.max_volunteers,
        points_reward=data.points_reward,
        hours_reward=data.hours_reward,
        created_by=created_by
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


def update_event(db: Session, event: Event, data: EventUpdate):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(event, field, value)

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


def register_for_event(db: Session, event: Event, user_id):
    existing = db.query(EventRegistration).filter(
        EventRegistration.event_id == event.id,
        EventRegistration.user_id == user_id,
        EventRegistration.status != RegistrationStatus.CANCELLED
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Already registered for this event"
        )

    if event.max_volunteers is not None:
        current_count = db.query(EventRegistration).filter(
            EventRegistration.event_id == event.id,
            EventRegistration.status != RegistrationStatus.CANCELLED
        ).count()

        if current_count >= event.max_volunteers:
            raise HTTPException(
                status_code=400,
                detail="Event has reached maximum volunteers"
            )

    registration = EventRegistration(
        event_id=event.id,
        user_id=user_id
    )

    db.add(registration)
    db.commit()
    db.refresh(registration)

    return registration


def cancel_registration(db: Session, registration: EventRegistration):
    registration.status = RegistrationStatus.CANCELLED

    db.add(registration)
    db.commit()
    db.refresh(registration)

    return registration

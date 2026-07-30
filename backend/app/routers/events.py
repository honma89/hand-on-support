from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_user, get_current_admin
from app.models.user import User
from app.models.event import Event, EventStatus
from app.models.event_registration import EventRegistration

from app.schemas.event import (
    EventCreate,
    EventUpdate,
    EventResponse,
    EventRegistrationResponse,
    RegistrationStatusUpdate
)

from app.services.event_service import (
    create_event,
    update_event,
    register_for_event,
    cancel_registration
)

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


def _get_event_or_404(db: Session, event_id: str) -> Event:
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return event


@router.get("", response_model=list[EventResponse])
def list_events(
    status: EventStatus | None = None,
    department_id: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Event)

    if status:
        query = query.filter(Event.status == status)

    if department_id:
        query = query.filter(Event.department_id == department_id)

    return query.order_by(Event.event_date).all()


@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: str, db: Session = Depends(get_db)):
    return _get_event_or_404(db, event_id)


@router.post("", response_model=EventResponse)
def create_event_endpoint(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    return create_event(db, event, current_admin.id)


@router.patch("/{event_id}", response_model=EventResponse)
def update_event_endpoint(
    event_id: str,
    event_data: EventUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    event = _get_event_or_404(db, event_id)
    return update_event(db, event, event_data)


@router.post("/{event_id}/publish", response_model=EventResponse)
def publish_event(
    event_id: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    event = _get_event_or_404(db, event_id)
    event.status = EventStatus.PUBLISHED

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


@router.post("/{event_id}/register", response_model=EventRegistrationResponse)
def register_endpoint(
    event_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    event = _get_event_or_404(db, event_id)
    return register_for_event(db, event, current_user.id)


@router.delete("/{event_id}/register", response_model=EventRegistrationResponse)
def cancel_registration_endpoint(
    event_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    registration = db.query(EventRegistration).filter(
        EventRegistration.event_id == event_id,
        EventRegistration.user_id == current_user.id
    ).first()

    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    return cancel_registration(db, registration)


@router.get("/me/registrations", response_model=list[EventRegistrationResponse])
def my_registrations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(EventRegistration).filter(
        EventRegistration.user_id == current_user.id
    ).all()


@router.get(
    "/{event_id}/registrations",
    response_model=list[EventRegistrationResponse]
)
def list_event_registrations(
    event_id: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    return db.query(EventRegistration).filter(
        EventRegistration.event_id == event_id
    ).all()


@router.patch(
    "/{event_id}/registrations/{registration_id}",
    response_model=EventRegistrationResponse
)
def update_registration_status(
    event_id: str,
    registration_id: str,
    status_update: RegistrationStatusUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    registration = db.query(EventRegistration).filter(
        EventRegistration.id == registration_id,
        EventRegistration.event_id == event_id
    ).first()

    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    registration.status = status_update.status

    db.add(registration)
    db.commit()
    db.refresh(registration)

    return registration

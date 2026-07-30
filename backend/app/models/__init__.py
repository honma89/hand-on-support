# Importing every model module here (rather than relying on whichever
# router/service happens to import them first) is what makes SQLAlchemy's
# string-based relationship() references (e.g. Mapped["TierLevel"]) resolve
# correctly. Without this, a class that's never otherwise imported at
# runtime raises `InvalidRequestError: failed to locate a name` the first
# time any query touches a model with a relationship pointing at it.
#
# NOTE: `role` and `volunteer` have no corresponding tables yet (the
# f3a91c7b2e4d migration deliberately excluded them -- see its docstring).
# They're still imported here so that any future relationship() reference
# to them resolves; just don't query through those relationships until
# their tables actually exist.
from app.models import (  # noqa: F401
    activity,
    activity_category,
    activity_log,
    address,
    announcement,
    attendance,
    audit_log,
    badge,
    department,
    document,
    donation,
    dungkhag,
    dzongkhag,
    event,
    event_registration,
    gewog,
    location,
    media,
    notification,
    point_transaction,
    recognition,
    role,
    tier_level,
    user,
    user_badge,
    user_department,
    user_role,
    volunteer,
)

# Backend fix summary

The uploaded project contained two independently-generated backend systems
merged into one codebase: an async system (SQLAlchemy async, JWT+cookie
auth, repository/service pattern — what the Next.js frontend is actually
built against) and a second, incompatible "org schema" system (sync
SQLAlchemy, dzongkhag/dungkhag/gewog hierarchy, departments, volunteers,
donations, media, recognitions, etc.).

This has been fixed and **verified end-to-end** with an in-process HTTP
smoke test (register → login → create event → register for event → mark
attendance → points auto-awarded → badge auto-awarded → leaderboard →
notifications → admin dashboard → role-based 403). All checks passed.

## Root causes found and fixed

1. **`app/main.py`** — called `get_settings()` without importing it (would
   crash instantly), had duplicate router imports, and was missing CORS
   middleware entirely (would have silently broken the frontend's
   cookie-based login from the browser). Rewritten cleanly with a single
   import block, CORS configured from `settings.CORS_ORIGINS`, and only the
   routers the frontend actually uses.

2. **Four routers overwritten by the sync/org-schema system**:
   `app/routers/events.py`, `badges.py`, `admin.py`, `leaderboard.py` — all
   imported `app.database.session` (a *sync* SQLAlchemy engine pointed at
   an `asyncpg://` URL, which crashes on first use). Rewritten as async,
   using the existing repository/service layer.

3. **Matching services/schemas also overwritten**:
   `app/services/event_service.py`, `badge_service.py`, `point_service.py`,
   and `app/schemas/event.py`, `badge.py`, `admin.py` referenced org-schema
   models/fields that don't match the real `Event`/`Badge`/`User` models
   (e.g. `department_id`/`max_volunteers` instead of `category`/`capacity`).
   Rewritten to match the actual models, cross-checked directly against the
   frontend's TypeScript types (`frontend/src/lib/types/index.ts`) and
   hooks so response shapes line up exactly with what the UI expects.

   Note: `admin_repository.py`, `admin_service.py`, `leaderboard_service.py`,
   `registration_service.py`, and the `registrations.py`/`attendance.py`
   routers were **already correct** — only the layers listed above needed
   rewriting.

4. **Two independent Alembic migration chains with no common ancestor**
   (`alembic upgrade head` would hit an ambiguous-heads error). The
   orphaned chain (`17d747ed40f3` → `11131b566373`, belonging to the
   disconnected sync system) was moved to
   `backend/alembic/versions_unintegrated_legacy/` — preserved, not
   deleted. The active chain is now a single clean head:
   `e74810f03c36` → `f3a91c7b2e4d`.

5. **`app/models/address.py`** — missing `UUID` import (would crash on
   first use of any FK on that table) and a stray `relationship("Volunteer", ...)`
   pointing at the disconnected legacy model (would crash SQLAlchemy's
   mapper configuration on app startup). Both fixed. This model is part of
   the *active* migration chain (referenced by `User.address_id`), so this
   was a real, previously-unnoticed bug independent of the two-systems
   issue.

## What was intentionally left disconnected

13 routers belong exclusively to the org-schema system and are **not
called by the frontend anywhere** (confirmed by grepping every API call in
`frontend/src`): `volunteers`, `locations`, `departments`, `activities`,
`recognitions`, `media`, `documents`, `announcements`, `donations`, plus
their sync-only support files (`app/config.py`, `app/database/`,
`app/core/dependencies.py`, `app/core/jwt.py`). These are left in place,
untouched, but not imported into `main.py`. If you want that feature set
(a substantial separate scope — dzongkhag/dungkhag/gewog hierarchy,
volunteer records, donations, media library, etc.), it needs its own
dedicated integration pass: converting each router to the async
repository/service pattern and reconciling with the `User`/`Event` models
already in place.

## Verified working (via smoke test against an in-memory DB)

- `POST /api/v1/auth/register`, `/auth/login`, `/auth/me`
- `GET/POST/PATCH/DELETE /api/v1/events`, `/events/{id}`
- `POST /api/v1/events/{id}/register`, `DELETE .../register`
- `GET /api/v1/registrations/me`
- `POST /api/v1/events/{id}/attendance` (+ automatic point award + automatic
  badge award, idempotent via `points_awarded` guard)
- `GET /api/v1/badges`, `/badges/me`
- `GET /api/v1/leaderboard`
- `GET /api/v1/points/me/balance`, `/points/me/history`, `POST .../redeem`,
  `POST /admin/adjust`
- `GET /api/v1/notifications`, unread count, mark read
- `GET /api/v1/admin/dashboard` (and confirmed 403 for non-admins)
- Single-head Alembic chain, FastAPI OpenAPI schema builds cleanly, 45
  routes registered

## Not yet done (frontend)

The Stitch design (`stitch_hand_on_support_hub.zip`, 8 pages) has **not**
been integrated into the Next.js frontend yet. See the handoff prompt
provided alongside this zip for exactly what's needed next.

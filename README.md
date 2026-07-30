# Hand On Support

Volunteer management platform for Bhutan — connects volunteers with
community service opportunities and rewards participation via the
**Point Bank** gamification system.

## Stack

- **Frontend:** Next.js 15 (App Router), TypeScript, Tailwind CSS, shadcn/ui, TanStack Query, React Hook Form, Zod
- **Backend:** FastAPI, SQLAlchemy 2.0 (async), Alembic, Pydantic v2
- **Database:** PostgreSQL
- **Auth:** JWT access tokens + refresh tokens in HttpOnly cookies
- **Infra:** Docker, Docker Compose, Nginx

## Architecture

```
hand-on-support/
├── backend/                # FastAPI app (owns all business logic + DB access)
│   ├── app/
│   │   ├── core/           # config, security utilities
│   │   ├── db/             # engine, session, Base
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── schemas/        # Pydantic request/response schemas
│   │   ├── repositories/   # DB query layer (no business logic)
│   │   ├── services/       # business logic (uses repositories)
│   │   ├── routers/        # FastAPI route handlers (thin, call services)
│   │   └── main.py         # app entrypoint
│   └── alembic/            # DB migrations
├── frontend/                # Next.js app (never touches Postgres directly)
│   └── src/
│       ├── app/             # App Router pages/layouts
│       ├── components/      # UI + providers
│       └── lib/             # api client, utils
└── nginx/                   # reverse proxy: routes /api/* -> backend, / -> frontend
```

**Rule:** The frontend only ever talks to the backend over REST
(`/api/v1/...`). All business logic, validation, and persistence live in
FastAPI. Every backend module follows `router -> service -> repository -> model`.

## Local development (Docker Compose)

```bash
cp backend/.env.example backend/.env
# edit backend/.env and set a real JWT_SECRET_KEY

docker compose up --build
```

- App (via Nginx): http://localhost
- Backend API docs: http://localhost/api/docs
- Postgres: localhost:5432 (user/pass/db: `handonsupport`)

## Local development (without Docker)

**Backend**
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # point DATABASE_URL at a local Postgres
uvicorn app.main:app --reload
```

**Frontend**
```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

## Database migrations

```bash
cd backend
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

## Modules implemented so far

- [x] Module 0 — Project Foundation & Scaffolding
- [x] Module 1 — Authentication
- [x] Module 2 — User Profiles
- [x] Module 3 — Events
- [x] Module 4 — Event Registration
- [x] Module 5 — Attendance
- [x] Module 6 — Point Bank
- [x] Module 7 — Leaderboards
- [x] Module 8 — Badges
- [x] Module 9 — Admin Dashboard
- [x] Module 10 — Analytics
- [x] Module 11 — Notifications

All modules verified end-to-end against a real Postgres database via
`backend/scripts/smoke_test.py` (register → login → role promotion → badge
creation → event publish → registration → attendance → automatic point
award → automatic badge award → leaderboard → notifications → admin
dashboard → analytics). Frontend pages (login, register, events list/detail,
dashboard, leaderboard, notifications, admin dashboard) type-check and
production-build cleanly against this API contract.

### Known gaps / next steps
- Frontend: Badges catalog page, per-event attendance-marking UI for
  organizers/admins, and the `/register/redeem` point-redemption UI are not
  yet built (their backend endpoints exist and are fully tested).
- No automated `pytest` suite yet — `scripts/smoke_test.py` is a manual
  end-to-end script, not a CI-run test suite.
- No route-level auth guarding/middleware on the frontend yet (pages assume
  the visitor is logged in where relevant, but don't redirect unauthenticated
  users away from `/dashboard` etc.).
- `backend/.env` and `frontend/.env.local` are excluded from the zip —
  copy from the `.example` files before running.

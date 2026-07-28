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
- [ ] Module 1 — Authentication
- [ ] Module 2 — User Profiles
- [ ] Module 3 — Events
- [ ] Module 4 — Event Registration
- [ ] Module 5 — Attendance
- [ ] Module 6 — Point Bank
- [ ] Module 7 — Leaderboards
- [ ] Module 8 — Badges
- [ ] Module 9 — Admin Dashboard
- [ ] Module 10 — Analytics
- [ ] Module 11 — Notifications

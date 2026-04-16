# ReferIn

A full-stack job and referral platform where job seekers can browse aggregated job listings, request referrals from employees at target companies, and receive personalized job recommendations.

Built with **React + TypeScript** (frontend) and **FastAPI + SQLAlchemy** (backend).

---

## Features

- **Job Aggregation** — Browse 44 seeded jobs from companies like Google, Microsoft, Amazon, Meta, Netflix, and more
- **Full-Text Search** — Search jobs by keyword across title, company, and description
- **Filters** — Filter by location, job type (full-time/part-time/contract/internship), experience range, and remote
- **Referral System** — Job seekers request referrals; referrers accept or reject with in-app notifications
- **Smart Recommendations** — Rule-based scoring (40% skill match, 20% location, 20% experience, 20% popularity)
- **Notifications** — Real-time in-app notification system for referral status updates
- **JWT Authentication** — Register/login with role-based access control (job_seeker, referrer, admin)
- **Responsive UI** — Tailwind CSS with mobile-friendly layout

---

## Tech Stack

| Layer      | Technology                                                             |
| ---------- | ---------------------------------------------------------------------- |
| Frontend   | React 19, TypeScript, Tailwind CSS v4, Redux Toolkit, Vite 8           |
| Backend    | FastAPI, Python 3.11+, SQLAlchemy 2.0 (async), Pydantic v2             |
| Database   | SQLite (local dev via aiosqlite) / PostgreSQL (production via asyncpg) |
| Auth       | JWT tokens (python-jose + passlib/bcrypt)                              |
| State      | Redux Toolkit with 4 slices (auth, jobs, referrals, notifications)     |
| API Client | Axios with JWT interceptor for automatic token refresh                 |

---

## Prerequisites

- **Python 3.11+** (tested with 3.14)
- **Node.js 18+** and **npm**
- Git

> No Docker, PostgreSQL, or Redis required for local development. The app uses SQLite out of the box.

---

## Getting Started

### 1. Clone the repository

```bash
git clone <repo-url>
cd referIn
```

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

> **Note (Python 3.14+):** If `bcrypt` installation fails, pin it explicitly:
>
> ```bash
> pip install "bcrypt==4.0.1"
> ```

#### Configure environment (optional)

Copy the example env file and adjust values if needed:

```bash
cp .env.example .env
```

Available environment variables:

| Variable                      | Default                                             | Description             |
| ----------------------------- | --------------------------------------------------- | ----------------------- |
| `DATABASE_URL`                | `sqlite+aiosqlite:///.../backend/referin.db`        | Database connection URL |
| `SECRET_KEY`                  | `your-super-secret-key-change-in-production`        | JWT signing key         |
| `ALGORITHM`                   | `HS256`                                             | JWT algorithm           |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30`                                                | Token expiry in minutes |
| `CORS_ORIGINS`                | `["http://localhost:5173","http://localhost:3000"]` | Allowed CORS origins    |

#### Seed the database

```bash
python -m app.db.seed
```

This creates `backend/referin.db` with 5 test users and 44 jobs.

#### Start the backend server

```bash
uvicorn app.main:app --reload --port 8000
```

Verify it works:

```bash
curl http://localhost:8000/health
# {"status":"healthy","service":"ReferIn API"}
```

### 3. Frontend Setup

Open a **new terminal**:

```bash
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

### 4. Open the app

| Service         | URL                         |
| --------------- | --------------------------- |
| Frontend        | http://localhost:5173       |
| Backend API     | http://localhost:8000       |
| Swagger UI Docs | http://localhost:8000/docs  |
| ReDoc           | http://localhost:8000/redoc |

---

## Test Users

After seeding, these accounts are available:

| Email                | Password      | Role         | Description             |
| -------------------- | ------------- | ------------ | ----------------------- |
| `seeker@test.com`    | `password123` | `job_seeker` | Has React/Python skills |
| `seeker2@test.com`   | `password123` | `job_seeker` | Has Java/AWS skills     |
| `referrer@test.com`  | `password123` | `referrer`   | Python/FastAPI referrer |
| `referrer2@test.com` | `password123` | `referrer`   | React/Next.js referrer  |
| `admin@test.com`     | `password123` | `admin`      | Admin user              |

---

## API Endpoints

### Authentication

| Method | Endpoint                | Auth | Description         |
| ------ | ----------------------- | ---- | ------------------- |
| POST   | `/api/v1/auth/register` | No   | Register a new user |
| POST   | `/api/v1/auth/login`    | No   | Login, returns JWT  |
| GET    | `/api/v1/auth/me`       | Yes  | Get current user    |

### Jobs

| Method | Endpoint                   | Auth | Description                  |
| ------ | -------------------------- | ---- | ---------------------------- |
| GET    | `/api/v1/jobs`             | No   | List/search jobs (paginated) |
| GET    | `/api/v1/jobs/{id}`        | No   | Get job details              |
| GET    | `/api/v1/jobs/recommended` | Yes  | Personalized recommendations |

**Search query parameters:** `q`, `location`, `type`, `is_remote`, `experience_min`, `experience_max`, `page`, `size`

### Referrals

| Method | Endpoint                 | Auth | Description          |
| ------ | ------------------------ | ---- | -------------------- |
| POST   | `/api/v1/referrals`      | Yes  | Request a referral   |
| GET    | `/api/v1/referrals/my`   | Yes  | List sent & received |
| PATCH  | `/api/v1/referrals/{id}` | Yes  | Accept or reject     |

### Users

| Method | Endpoint                | Auth | Description         |
| ------ | ----------------------- | ---- | ------------------- |
| GET    | `/api/v1/users/{id}`    | No   | Public user profile |
| PUT    | `/api/v1/users/profile` | Yes  | Update own profile  |

### Notifications

| Method | Endpoint                          | Auth | Description        |
| ------ | --------------------------------- | ---- | ------------------ |
| GET    | `/api/v1/notifications`           | Yes  | List notifications |
| PATCH  | `/api/v1/notifications/{id}/read` | Yes  | Mark as read       |

---

## Project Structure

```
referIn/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py              # Auth dependencies (get_current_user, require_role)
│   │   │   └── v1/                  # Route handlers (auth, jobs, referrals, users, notifications)
│   │   ├── core/
│   │   │   ├── config.py            # Pydantic settings (env vars)
│   │   │   ├── constants.py         # App constants and recommendation weights
│   │   │   └── security.py          # JWT token + password hashing
│   │   ├── db/
│   │   │   ├── database.py          # Async engine, session factory, Base
│   │   │   └── seed.py              # Database seeding script
│   │   ├── models/                  # SQLAlchemy ORM models (user, job, referral, notification)
│   │   ├── schemas/                 # Pydantic request/response schemas
│   │   ├── services/                # Business logic layer
│   │   ├── repositories/            # Data access layer
│   │   ├── tasks/                   # Celery background tasks (optional)
│   │   └── main.py                  # FastAPI app entry point
│   ├── tests/                       # pytest async tests
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.ts            # Axios instance with JWT interceptor
│   │   ├── components/              # Reusable UI components (Navbar, JobCard, etc.)
│   │   ├── pages/                   # Page components (Auth, Jobs, Referrals, etc.)
│   │   ├── store/                   # Redux Toolkit store + slices
│   │   ├── types/                   # TypeScript interfaces
│   │   ├── routes/
│   │   │   └── AppRouter.tsx        # React Router v6 route definitions
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── Dockerfile
├── docs/                            # Specification documents
│   ├── PRD.md                       # Product Requirements Document
│   ├── API_SPEC.md                  # Full API specification
│   ├── DATABASE_SCHEMA.md           # Database schema design
│   ├── ARCHITECTURE.md              # Architecture decisions
│   └── IMPLEMENTATION_SPEC.md       # Implementation details
├── docker-compose.yml               # Full stack orchestration (PostgreSQL + Redis)
└── README.md
```

---

## Architecture

The backend follows a **clean layered architecture**:

```
HTTP Request
  → API Route (controller)
    → Service (business logic)
      → Repository (data access)
        → SQLAlchemy Model (ORM)
```

The frontend uses **Redux Toolkit** for state management with feature-based slices:

```
User Action
  → Redux Dispatch (async thunk)
    → Axios API Client (with JWT interceptor)
      → Backend API
    → Redux Slice Reducer
  → React Component Re-render
```

---

## Running Tests

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/test_auth.py
pytest tests/test_jobs.py
pytest tests/test_referrals.py
pytest tests/test_recommendations.py
```

---

## Building for Production

### Frontend

```bash
cd frontend
npm run build
# Output in frontend/dist/
```

### Docker (PostgreSQL + Redis)

If Docker is available, the full stack can run with:

```bash
docker-compose up --build
docker-compose exec backend python -m app.db.seed
```

Set `DATABASE_URL` to a PostgreSQL connection string in `.env` for production:

```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/referin
```

---

## Common Issues

| Issue                                        | Solution                                                  |
| -------------------------------------------- | --------------------------------------------------------- |
| `bcrypt` / `passlib` error on Python 3.14+   | `pip install "bcrypt==4.0.1"`                             |
| `ModuleNotFoundError: No module named 'app'` | Make sure you run `uvicorn` from the `backend/` directory |
| Empty jobs list after starting server        | Run `python -m app.db.seed` from `backend/` first         |
| CORS errors in browser                       | Ensure backend is on port 8000 and frontend on 5173       |
| `aiosqlite` not found                        | `pip install aiosqlite` (already in requirements.txt)     |

---

## Documentation

- [Product Requirements Document](docs/PRD.md)
- [API Specification](docs/API_SPEC.md)
- [Database Schema](docs/DATABASE_SCHEMA.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Implementation Spec](docs/IMPLEMENTATION_SPEC.md)

---

## License

MIT

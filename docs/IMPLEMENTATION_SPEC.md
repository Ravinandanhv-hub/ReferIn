# ReferIn – Complete Implementation Specification

> **Use this file to generate the full ReferIn application in agent mode.**
> All decisions, architecture, data models, APIs, and file structures are specified below.

---

## 1. Project Overview

**ReferIn** is a full-stack job and referral platform.

| Layer            | Technology                                                               |
| ---------------- | ------------------------------------------------------------------------ |
| Frontend         | React 18, TypeScript, Tailwind CSS, Redux Toolkit, Vite, React Router v6 |
| Backend          | FastAPI (Python 3.11), SQLAlchemy 2.0 (async), Pydantic v2               |
| Database         | PostgreSQL 16 with full-text search (tsvector + GIN index)               |
| Cache/Queue      | Redis 7                                                                  |
| Background Jobs  | Celery                                                                   |
| Auth             | JWT (python-jose + passlib/bcrypt)                                       |
| Containerization | Docker + Docker Compose                                                  |
| Testing          | Pytest (async), aiosqlite for test DB                                    |

---

## 2. Architecture

```
Frontend (React + Vite :5173)
     │ Axios + JWT
     ▼
Backend (FastAPI :8000)
  ├── API Layer (app/api/v1/) — route handlers, auth deps
  ├── Service Layer (app/services/) — business logic
  ├── Repository Layer (app/repositories/) — DB queries
  ├── Model Layer (app/models/) — SQLAlchemy ORM
  └── Schema Layer (app/schemas/) — Pydantic validation
     │
     ▼
PostgreSQL 16 + Redis 7 (Celery broker)
```

**Clean architecture**: Controllers → Services → Repositories → Models. No business logic in controllers or repositories.

---

## 3. Database Schema

### users

- id: UUID PK
- name: VARCHAR(255) NOT NULL
- email: VARCHAR(255) UNIQUE NOT NULL (indexed)
- hashed_password: VARCHAR(255) NOT NULL
- role: VARCHAR(20) NOT NULL DEFAULT 'job_seeker' CHECK IN ('job_seeker','referrer','admin')
- skills: TEXT[] DEFAULT '{}'
- experience: INTEGER DEFAULT 0
- resume_url: TEXT NULL
- location: VARCHAR(255) NULL
- preferences: JSONB DEFAULT '{}'
- created_at: TIMESTAMPTZ DEFAULT NOW()
- updated_at: TIMESTAMPTZ DEFAULT NOW()

### jobs

- id: UUID PK
- title: VARCHAR(500) NOT NULL
- company: VARCHAR(255) NOT NULL
- location: VARCHAR(255) NULL
- type: VARCHAR(20) NOT NULL DEFAULT 'full_time' CHECK IN ('full_time','part_time','contract','internship')
- skills_required: TEXT[] DEFAULT '{}'
- description: TEXT NULL
- source: VARCHAR(100) NULL
- apply_url: TEXT NULL
- is_remote: BOOLEAN DEFAULT FALSE
- experience_min: INTEGER DEFAULT 0
- experience_max: INTEGER DEFAULT 0
- posted_at: TIMESTAMPTZ DEFAULT NOW()
- search_vector: TSVECTOR (GIN indexed, auto-updated via trigger)
- created_at: TIMESTAMPTZ DEFAULT NOW()

**Search vector trigger**: Weights `title(A)`, `company(B)`, `description(C)`, `location(D)`.

### referrals

- id: UUID PK
- job_id: UUID FK→jobs(id) CASCADE
- requester_id: UUID FK→users(id) CASCADE
- referrer_id: UUID FK→users(id) CASCADE
- status: VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK IN ('pending','accepted','rejected')
- message: TEXT NULL
- created_at: TIMESTAMPTZ DEFAULT NOW()
- updated_at: TIMESTAMPTZ DEFAULT NOW()
- UNIQUE(job_id, requester_id, referrer_id)
- CHECK(requester_id != referrer_id)

### notifications

- id: UUID PK
- user_id: UUID FK→users(id) CASCADE
- type: VARCHAR(50) NOT NULL
- title: VARCHAR(255) NOT NULL
- message: TEXT NULL
- is_read: BOOLEAN DEFAULT FALSE
- created_at: TIMESTAMPTZ DEFAULT NOW()

---

## 4. API Endpoints (All under /api/v1)

### Auth

| Method | Path           | Auth | Description                                           |
| ------ | -------------- | ---- | ----------------------------------------------------- |
| POST   | /auth/register | No   | Register (name, email, password, role) → UserResponse |
| POST   | /auth/login    | No   | Login (email, password) → {access_token, token_type}  |
| GET    | /auth/me       | Yes  | Get current user → UserResponse                       |

### Jobs

| Method | Path              | Auth | Description                                                                          |
| ------ | ----------------- | ---- | ------------------------------------------------------------------------------------ |
| GET    | /jobs             | No   | List/search (q, location, type, is_remote, exp_min, exp_max, page, size) → paginated |
| GET    | /jobs/recommended | Yes  | Personalized recommendations (limit)                                                 |
| GET    | /jobs/{id}        | No   | Job detail                                                                           |

### Referrals

| Method | Path            | Auth | Description                                   |
| ------ | --------------- | ---- | --------------------------------------------- |
| POST   | /referrals      | Yes  | Create request (job_id, referrer_id, message) |
| GET    | /referrals/my   | Yes  | Get sent + received (status filter)           |
| PATCH  | /referrals/{id} | Yes  | Accept/reject (only referrer)                 |

### Users

| Method | Path           | Auth | Description        |
| ------ | -------------- | ---- | ------------------ |
| GET    | /users/{id}    | No   | Public profile     |
| PUT    | /users/profile | Yes  | Update own profile |

### Notifications

| Method | Path                     | Auth | Description               |
| ------ | ------------------------ | ---- | ------------------------- |
| GET    | /notifications           | Yes  | List (unread_only filter) |
| PATCH  | /notifications/{id}/read | Yes  | Mark as read              |

---

## 5. Recommendation Algorithm (Rule-Based)

```
Score = skill_match × 0.4 + location_match × 0.2 + experience_fit × 0.2 + popularity × 0.2
```

- **skill_match**: |user_skills ∩ job_skills| / |job_skills| (0-1)
- **location_match**: 1.0 if remote or exact match, 0.7 if preferred location, 0 otherwise
- **experience_fit**: 1.0 if within range, decreasing based on gap
- **popularity**: 0.5 (placeholder, use recency proxy)

Output includes `score` (float) and `match_reasons` (list of strings).

---

## 6. Folder Structure

```
referIn/
├── docs/PRD.md, API_SPEC.md, DATABASE_SCHEMA.md, ARCHITECTURE.md
├── backend/
│   ├── app/
│   │   ├── api/v1/ (auth.py, jobs.py, referrals.py, users.py, notifications.py)
│   │   ├── api/deps.py (get_current_user, require_role)
│   │   ├── core/ (config.py, security.py, constants.py)
│   │   ├── models/ (user.py, job.py, referral.py, notification.py)
│   │   ├── schemas/ (user.py, job.py, referral.py, notification.py)
│   │   ├── services/ (auth_service.py, job_service.py, referral_service.py, recommendation_service.py, notification_service.py)
│   │   ├── repositories/ (user_repo.py, job_repo.py, referral_repo.py, notification_repo.py)
│   │   ├── tasks/ (celery_app.py, job_tasks.py)
│   │   ├── db/ (database.py, seed.py, migrations/)
│   │   └── main.py
│   ├── tests/ (conftest.py, test_auth.py, test_jobs.py, test_referrals.py, test_recommendations.py)
│   ├── requirements.txt, Dockerfile, alembic.ini, .env.example
├── frontend/
│   ├── src/
│   │   ├── api/ (client.ts, authApi.ts, jobsApi.ts, referralsApi.ts, usersApi.ts)
│   │   ├── components/layout/ (Navbar.tsx, Footer.tsx)
│   │   ├── components/jobs/ (JobCard.tsx, JobFilters.tsx)
│   │   ├── pages/ (AuthPage.tsx, DashboardPage.tsx, JobsPage.tsx, JobDetailsPage.tsx, ReferralsPage.tsx, ProfilePage.tsx)
│   │   ├── store/ (store.ts, authSlice.ts, jobsSlice.ts, referralsSlice.ts, userSlice.ts)
│   │   ├── hooks/ (useAppStore.ts)
│   │   ├── types/ (user.ts, job.ts, referral.ts, api.ts)
│   │   ├── routes/ (AppRouter.tsx)
│   │   ├── App.tsx, main.tsx, index.css
│   ├── Dockerfile, nginx.conf, .env.example
├── docker-compose.yml, .gitignore, README.md
```

---

## 7. Seed Data

- **5 test users**: seeker@test.com, seeker2@test.com, referrer@test.com, referrer2@test.com, admin@test.com (all password: password123)
- **50+ mock jobs**: Across Google, Microsoft, Amazon, Meta, Netflix, Spotify, Uber, and startups. Mix of full_time, part_time, contract, internship. Various locations + remote. Diverse skills.

---

## 8. Docker Compose Services

| Service       | Image              | Port | Depends On |
| ------------- | ------------------ | ---- | ---------- |
| db            | postgres:16-alpine | 5432 | -          |
| redis         | redis:7-alpine     | 6379 | -          |
| backend       | ./backend          | 8000 | db, redis  |
| celery_worker | ./backend          | -    | db, redis  |
| frontend      | ./frontend         | 80   | backend    |

---

## 9. MVP Scope (Phase 1)

✅ Email/password JWT auth  
✅ Job listing with 50+ seeded mock jobs  
✅ PostgreSQL full-text search (tsvector)  
✅ Rule-based recommendations  
✅ Referral request/accept/reject with notifications  
✅ In-app notification system  
✅ Search with filters (location, type, experience, remote)  
✅ Docker + docker-compose  
✅ Swagger API docs at /docs  
✅ Backend tests (pytest)

---

## 10. How to Run

```bash
# With Docker
docker-compose up --build
docker-compose exec backend python -m app.db.seed

# Frontend: http://localhost (port 80)
# Backend API: http://localhost:8000
# Swagger Docs: http://localhost:8000/docs

# Local Dev (backend)
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Local Dev (frontend)
cd frontend && npm install && npm run dev
```

# ReferIn – Architecture Document

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (React)                   │
│          Vite + TypeScript + Tailwind CSS            │
│              Redux Toolkit + React Router            │
│                   Port: 5173                         │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP (Axios)
                       ▼
┌─────────────────────────────────────────────────────┐
│                Backend (FastAPI)                      │
│              Python 3.11 + Async                     │
│           JWT Auth + Swagger Docs                    │
│                   Port: 8000                         │
├──────────────────────┬──────────────────────────────┤
│   API Layer (v1)     │   Services Layer             │
│   ├── auth           │   ├── auth_service           │
│   ├── jobs           │   ├── job_service            │
│   ├── referrals      │   ├── referral_service       │
│   ├── users          │   ├── recommendation_service │
│   └── notifications  │   └── notification_service   │
├──────────────────────┼──────────────────────────────┤
│   Repository Layer   │   Background Tasks           │
│   ├── user_repo      │   ├── Celery Worker          │
│   ├── job_repo       │   └── Redis Broker           │
│   ├── referral_repo  │                              │
│   └── notif_repo     │                              │
└──────────────────────┴──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              PostgreSQL 16 + Redis 7                 │
│   ├── users, jobs, referrals, notifications         │
│   ├── Full-text search (tsvector + GIN)             │
│   └── Redis: Celery broker + result backend         │
└─────────────────────────────────────────────────────┘
```

## Clean Architecture Layers

### 1. API Layer (`app/api/v1/`)

- Route handlers (controllers)
- Request validation (Pydantic schemas)
- Response serialization
- Authentication dependencies
- No business logic here

### 2. Service Layer (`app/services/`)

- Business logic and validation
- Orchestrates repositories
- Computes recommendations
- Manages referral state transitions
- Triggers notifications

### 3. Repository Layer (`app/repositories/`)

- Database access (SQLAlchemy async)
- CRUD operations
- Query builders
- No business logic

### 4. Model Layer (`app/models/`)

- SQLAlchemy ORM models
- Database table definitions
- Relationships and constraints

### 5. Schema Layer (`app/schemas/`)

- Pydantic models for request/response
- Input validation
- Serialization

## Key Design Decisions

| Decision         | Choice                      | Rationale                               |
| ---------------- | --------------------------- | --------------------------------------- |
| Web Framework    | FastAPI                     | Async, auto-docs, Pydantic integration  |
| ORM              | SQLAlchemy 2.0 (async)      | Mature, async support, type hints       |
| Database         | PostgreSQL 16               | Full-text search, JSONB, arrays, robust |
| Search           | PG full-text (tsvector)     | No extra infra, sufficient for MVP      |
| Auth             | JWT (python-jose + passlib) | Stateless, scalable                     |
| State Management | Redux Toolkit               | User preference, structured state       |
| Background Jobs  | Celery + Redis              | Proven, Python-native                   |
| Containerization | Docker Compose              | Local dev parity with production        |

## Security

- Passwords hashed with bcrypt (12 rounds)
- JWT tokens with expiration (30 min access)
- CORS whitelist configured
- SQL injection prevented via parameterized queries (SQLAlchemy)
- Input validation via Pydantic
- Role-based access control on endpoints

## API Versioning

All APIs are versioned under `/api/v1/`. Future breaking changes will be introduced under `/api/v2/`.

## Scalability Path

Phase 1 (monolith) → Phase 2 (modular monolith) → Phase 3 (microservices):

- Services are already decoupled via clean architecture
- Each service can be extracted into its own microservice
- Redis already in place for async communication
- PostgreSQL can be scaled vertically, then sharded

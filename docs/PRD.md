# ReferIn – Product Requirements Document (PRD)

## 1. Product Overview

**Product Name:** ReferIn  
**Type:** Full-stack web application (scalable SaaS)  
**Goal:** A centralized platform where users can find jobs globally, request & provide referrals, get AI-powered job recommendations, and view jobs aggregated from company career pages + job portals.

## 2. Core Objectives

- Aggregate jobs from multiple sources into one platform
- Enable referral-based hiring ecosystem
- Provide personalized job recommendations using rule-based scoring (Phase 1) and AI (Phase 2)
- Improve job discovery efficiency
- Build a scalable, production-ready system

## 3. User Roles

### 3.1 Job Seeker

- Register/Login
- Create profile (skills, experience, resume)
- Browse/search jobs
- Request referrals
- Track applications

### 3.2 Referrer (Employee)

- Post referral opportunities
- Accept/reject referral requests
- Track referrals given

### 3.3 Admin

- Manage users
- Moderate jobs/referrals
- Monitor system health
- _(Phase 1: Backend APIs only, admin UI deferred to Phase 2)_

## 4. Core Features

### 4.1 Authentication & User Management

- Email/password login with JWT tokens
- Role-based access control (job_seeker, referrer, admin)
- Profile management (skills, experience, location, preferences)

### 4.2 Job Aggregation Engine

- Phase 1: Seeded mock data (50+ jobs across multiple companies)
- Phase 2: Web scraping, API integration (LinkedIn, Indeed, etc.)
- Deduplication and normalization of job data
- PostgreSQL full-text search with tsvector/tsquery

### 4.3 Referral System

- Job seekers can request referrals for specific jobs
- Referrers can accept or reject referral requests
- Status tracking: pending → accepted / rejected
- Validation: no self-referrals, no duplicate requests

### 4.4 Job Recommendation Engine

- **Phase 1 (Rule-based):**
  - Score = skill_match × 0.4 + location_match × 0.2 + experience_fit × 0.2 + popularity × 0.2
- **Phase 2 (AI-based):**
  - Embeddings (OpenAI / vector DB)
  - Collaborative filtering

### 4.5 Search & Filtering

- Keyword search (PostgreSQL full-text search)
- Filters: location, experience, job type, remote toggle
- Paginated results

### 4.6 Notifications

- In-app notifications (Phase 1)
- Referral status updates
- New job alerts (Phase 2)
- Email notifications (Phase 2)

## 5. Data Models

### User

| Field           | Type                              |
| --------------- | --------------------------------- |
| id              | UUID (PK)                         |
| name            | string                            |
| email           | string (unique, indexed)          |
| hashed_password | string                            |
| role            | enum: job_seeker, referrer, admin |
| skills          | string[]                          |
| experience      | integer                           |
| resume_url      | string (nullable)                 |
| location        | string (nullable)                 |
| preferences     | JSONB                             |
| created_at      | timestamp                         |
| updated_at      | timestamp                         |

### Job

| Field           | Type                                             |
| --------------- | ------------------------------------------------ |
| id              | UUID (PK)                                        |
| title           | string                                           |
| company         | string                                           |
| location        | string                                           |
| type            | enum: full_time, part_time, contract, internship |
| skills_required | string[]                                         |
| description     | text                                             |
| source          | string                                           |
| apply_url       | string                                           |
| posted_at       | timestamp                                        |
| is_remote       | boolean                                          |
| experience_min  | integer                                          |
| experience_max  | integer                                          |
| search_vector   | tsvector (GIN indexed)                           |
| created_at      | timestamp                                        |

### Referral

| Field        | Type                              |
| ------------ | --------------------------------- |
| id           | UUID (PK)                         |
| job_id       | UUID (FK → jobs)                  |
| requester_id | UUID (FK → users)                 |
| referrer_id  | UUID (FK → users)                 |
| status       | enum: pending, accepted, rejected |
| message      | text                              |
| created_at   | timestamp                         |
| updated_at   | timestamp                         |

### Notification

| Field      | Type              |
| ---------- | ----------------- |
| id         | UUID (PK)         |
| user_id    | UUID (FK → users) |
| type       | string            |
| title      | string            |
| message    | text              |
| is_read    | boolean           |
| created_at | timestamp         |

## 6. Non-Functional Requirements

- Scalable (microservices-ready architecture)
- Secure (JWT, bcrypt passwords, input validation)
- Fast (<300ms API response target)
- Async APIs via FastAPI
- Background job processing via Celery + Redis
- Docker containerization for consistent environments

## 7. Phase 1 MVP Scope

✅ Email/password auth with JWT  
✅ Job listing with seeded mock data  
✅ PostgreSQL full-text search  
✅ Rule-based recommendations  
✅ Referral request/accept/reject  
✅ In-app notifications  
✅ Docker + docker-compose  
✅ Swagger API documentation  
✅ Seed scripts

## 8. Phase 2 Enhancements

- OAuth (Google, LinkedIn)
- AI recommendations (embeddings)
- Resume parsing
- Chat system (WebSocket)
- Real-time notifications
- Elasticsearch
- Admin dashboard UI
- Company dashboards
- Email notifications

# ReferIn – API Specification

**Base URL:** `/api/v1`  
**Auth:** Bearer JWT token in `Authorization` header  
**Content-Type:** `application/json`

---

## Authentication APIs

### POST /api/v1/auth/register

Register a new user.

**Request Body:**

```json
{
  "name": "string",
  "email": "string",
  "password": "string (min 8 chars)",
  "role": "job_seeker | referrer"
}
```

**Response (201):**

```json
{
  "id": "uuid",
  "name": "string",
  "email": "string",
  "role": "string",
  "created_at": "timestamp"
}
```

### POST /api/v1/auth/login

Login and receive JWT token.

**Request Body:**

```json
{
  "email": "string",
  "password": "string"
}
```

**Response (200):**

```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

### GET /api/v1/auth/me

Get current authenticated user profile.

**Auth Required:** Yes

**Response (200):**

```json
{
  "id": "uuid",
  "name": "string",
  "email": "string",
  "role": "string",
  "skills": ["string"],
  "experience": 0,
  "location": "string",
  "preferences": {},
  "created_at": "timestamp"
}
```

---

## Job APIs

### GET /api/v1/jobs

List jobs with search and filters.

**Query Params:**
| Param | Type | Description |
|-------|------|-------------|
| q | string | Full-text search query |
| location | string | Filter by location |
| type | string | full_time, part_time, contract, internship |
| is_remote | boolean | Filter remote jobs |
| experience_min | integer | Minimum experience |
| experience_max | integer | Maximum experience |
| page | integer | Page number (default: 1) |
| size | integer | Page size (default: 20, max: 100) |

**Response (200):**

```json
{
  "items": [
    {
      "id": "uuid",
      "title": "string",
      "company": "string",
      "location": "string",
      "type": "string",
      "skills_required": ["string"],
      "is_remote": false,
      "experience_min": 0,
      "experience_max": 5,
      "posted_at": "timestamp",
      "source": "string"
    }
  ],
  "total": 100,
  "page": 1,
  "size": 20,
  "pages": 5
}
```

### GET /api/v1/jobs/{id}

Get job details by ID.

**Response (200):**

```json
{
  "id": "uuid",
  "title": "string",
  "company": "string",
  "location": "string",
  "type": "string",
  "skills_required": ["string"],
  "description": "string",
  "source": "string",
  "apply_url": "string",
  "is_remote": false,
  "experience_min": 0,
  "experience_max": 5,
  "posted_at": "timestamp",
  "created_at": "timestamp"
}
```

### GET /api/v1/jobs/recommended

Get personalized job recommendations.

**Auth Required:** Yes

**Query Params:**
| Param | Type | Description |
|-------|------|-------------|
| limit | integer | Max results (default: 10) |

**Response (200):**

```json
{
  "items": [
    {
      "id": "uuid",
      "title": "string",
      "company": "string",
      "location": "string",
      "type": "string",
      "skills_required": ["string"],
      "score": 0.85,
      "match_reasons": ["skill_match: React, TypeScript", "location_match"]
    }
  ]
}
```

---

## Referral APIs

### POST /api/v1/referrals

Create a referral request.

**Auth Required:** Yes

**Request Body:**

```json
{
  "job_id": "uuid",
  "referrer_id": "uuid",
  "message": "string"
}
```

**Response (201):**

```json
{
  "id": "uuid",
  "job_id": "uuid",
  "requester_id": "uuid",
  "referrer_id": "uuid",
  "status": "pending",
  "message": "string",
  "created_at": "timestamp"
}
```

### GET /api/v1/referrals/my

Get my referrals (sent and received).

**Auth Required:** Yes

**Query Params:**
| Param | Type | Description |
|-------|------|-------------|
| type | string | "sent" or "received" |
| status | string | pending, accepted, rejected |

**Response (200):**

```json
{
  "sent": [...],
  "received": [...]
}
```

### PATCH /api/v1/referrals/{id}

Update referral status (accept/reject). Only the referrer can update.

**Auth Required:** Yes

**Request Body:**

```json
{
  "status": "accepted | rejected"
}
```

**Response (200):**

```json
{
  "id": "uuid",
  "status": "accepted",
  "updated_at": "timestamp"
}
```

---

## User APIs

### GET /api/v1/users/{id}

Get user public profile.

**Response (200):**

```json
{
  "id": "uuid",
  "name": "string",
  "role": "string",
  "skills": ["string"],
  "experience": 0,
  "location": "string"
}
```

### PUT /api/v1/users/profile

Update own profile.

**Auth Required:** Yes

**Request Body:**

```json
{
  "name": "string",
  "skills": ["string"],
  "experience": 0,
  "location": "string",
  "resume_url": "string",
  "preferences": {
    "job_type": ["remote", "full_time"],
    "locations": ["India", "US"]
  }
}
```

---

## Notification APIs

### GET /api/v1/notifications

Get user notifications.

**Auth Required:** Yes

**Query Params:**
| Param | Type | Description |
|-------|------|-------------|
| unread_only | boolean | Filter unread only |

**Response (200):**

```json
{
  "items": [
    {
      "id": "uuid",
      "type": "referral_request",
      "title": "New Referral Request",
      "message": "string",
      "is_read": false,
      "created_at": "timestamp"
    }
  ]
}
```

### PATCH /api/v1/notifications/{id}/read

Mark notification as read.

**Auth Required:** Yes

**Response (200):**

```json
{
  "id": "uuid",
  "is_read": true
}
```

---

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message string"
}
```

| Status Code | Description                             |
| ----------- | --------------------------------------- |
| 400         | Bad Request – Invalid input             |
| 401         | Unauthorized – Missing or invalid token |
| 403         | Forbidden – Insufficient permissions    |
| 404         | Not Found – Resource not found          |
| 409         | Conflict – Duplicate resource           |
| 422         | Validation Error – Invalid request body |
| 500         | Internal Server Error                   |

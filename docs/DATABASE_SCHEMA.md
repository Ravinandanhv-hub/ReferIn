# ReferIn – Database Schema

## Database: PostgreSQL 16

### Extensions

- `uuid-ossp` – UUID generation
- `pg_trgm` – Trigram matching (optional, for fuzzy search)

---

## Tables

### users

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'job_seeker'
        CHECK (role IN ('job_seeker', 'referrer', 'admin')),
    skills TEXT[] DEFAULT '{}',
    experience INTEGER DEFAULT 0,
    resume_url TEXT,
    location VARCHAR(255),
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_skills ON users USING GIN(skills);
```

### jobs

```sql
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    company VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    type VARCHAR(20) NOT NULL DEFAULT 'full_time'
        CHECK (type IN ('full_time', 'part_time', 'contract', 'internship')),
    skills_required TEXT[] DEFAULT '{}',
    description TEXT,
    source VARCHAR(100),
    apply_url TEXT,
    is_remote BOOLEAN DEFAULT FALSE,
    experience_min INTEGER DEFAULT 0,
    experience_max INTEGER DEFAULT 0,
    posted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    search_vector TSVECTOR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_jobs_company ON jobs(company);
CREATE INDEX idx_jobs_location ON jobs(location);
CREATE INDEX idx_jobs_type ON jobs(type);
CREATE INDEX idx_jobs_skills ON jobs USING GIN(skills_required);
CREATE INDEX idx_jobs_search ON jobs USING GIN(search_vector);
CREATE INDEX idx_jobs_posted_at ON jobs(posted_at DESC);

-- Trigger to auto-update search_vector
CREATE OR REPLACE FUNCTION jobs_search_vector_update() RETURNS trigger AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.company, '')), 'B') ||
        setweight(to_tsvector('english', COALESCE(NEW.description, '')), 'C') ||
        setweight(to_tsvector('english', COALESCE(NEW.location, '')), 'D');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER jobs_search_vector_trigger
    BEFORE INSERT OR UPDATE ON jobs
    FOR EACH ROW EXECUTE FUNCTION jobs_search_vector_update();
```

### referrals

```sql
CREATE TABLE referrals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    requester_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    referrer_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'accepted', 'rejected')),
    message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_referral UNIQUE(job_id, requester_id, referrer_id),
    CONSTRAINT no_self_referral CHECK (requester_id != referrer_id)
);

CREATE INDEX idx_referrals_requester ON referrals(requester_id);
CREATE INDEX idx_referrals_referrer ON referrals(referrer_id);
CREATE INDEX idx_referrals_job ON referrals(job_id);
CREATE INDEX idx_referrals_status ON referrals(status);
```

### notifications

```sql
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_unread ON notifications(user_id, is_read) WHERE is_read = FALSE;
```

---

## Entity Relationship Diagram (Text)

```
users (1) ──── (N) referrals.requester_id
users (1) ──── (N) referrals.referrer_id
jobs  (1) ──── (N) referrals.job_id
users (1) ──── (N) notifications.user_id
```

## Constraints Summary

| Table         | Constraint                                | Description                            |
| ------------- | ----------------------------------------- | -------------------------------------- |
| users         | UNIQUE(email)                             | No duplicate emails                    |
| referrals     | UNIQUE(job_id, requester_id, referrer_id) | No duplicate referral requests         |
| referrals     | CHECK(requester_id != referrer_id)        | Cannot self-refer                      |
| referrals     | FK → jobs(id) CASCADE                     | Delete referrals when job deleted      |
| referrals     | FK → users(id) CASCADE                    | Delete referrals when user deleted     |
| notifications | FK → users(id) CASCADE                    | Delete notifications when user deleted |

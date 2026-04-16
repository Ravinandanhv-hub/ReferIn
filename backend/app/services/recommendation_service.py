from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.job import Job
from app.repositories.job_repo import JobRepository
from app.schemas.job import RecommendedJobResponse, RecommendedJobListResponse
from app.core.constants import (
    SKILL_MATCH_WEIGHT,
    LOCATION_MATCH_WEIGHT,
    EXPERIENCE_MATCH_WEIGHT,
    POPULARITY_WEIGHT,
)


class RecommendationService:
    def __init__(self, db: AsyncSession):
        self.repo = JobRepository(db)

    async def get_recommendations(
        self, user: User, limit: int = 10
    ) -> RecommendedJobListResponse:
        # Get candidate jobs — prefer jobs matching user skills
        if user.skills:
            candidates = await self.repo.get_jobs_by_skills(user.skills, limit=100)
        else:
            candidates = await self.repo.get_all_jobs()

        # Score each job
        scored_jobs: list[tuple[Job, float, list[str]]] = []
        for job in candidates:
            score, reasons = self._compute_score(user, job)
            scored_jobs.append((job, score, reasons))

        # Sort by score descending
        scored_jobs.sort(key=lambda x: x[1], reverse=True)

        items = []
        for job, score, reasons in scored_jobs[:limit]:
            item = RecommendedJobResponse(
                id=job.id,
                title=job.title,
                company=job.company,
                location=job.location,
                type=job.type,
                skills_required=job.skills_required or [],
                is_remote=job.is_remote,
                experience_min=job.experience_min,
                experience_max=job.experience_max,
                posted_at=job.posted_at,
                source=job.source,
                score=round(score, 2),
                match_reasons=reasons,
            )
            items.append(item)

        return RecommendedJobListResponse(items=items)

    def _compute_score(self, user: User, job: Job) -> tuple[float, list[str]]:
        reasons: list[str] = []
        score = 0.0

        # Skill match
        user_skills = set(s.lower() for s in (user.skills or []))
        job_skills = set(s.lower() for s in (job.skills_required or []))

        if job_skills:
            overlap = user_skills & job_skills
            skill_score = len(overlap) / len(job_skills)
            score += SKILL_MATCH_WEIGHT * skill_score
            if overlap:
                reasons.append(f"skill_match: {', '.join(overlap)}")
        else:
            score += SKILL_MATCH_WEIGHT * 0.5  # Neutral if no skills specified

        # Location match
        user_location = (user.location or "").lower()
        job_location = (job.location or "").lower()
        user_pref_locations = [
            loc.lower()
            for loc in (user.preferences or {}).get("locations", [])
        ]

        location_score = 0.0
        if job.is_remote:
            location_score = 1.0
            reasons.append("remote_job")
        elif user_location and job_location and user_location in job_location:
            location_score = 1.0
            reasons.append("location_match")
        elif any(loc in job_location for loc in user_pref_locations if loc):
            location_score = 0.7
            reasons.append("preferred_location")

        score += LOCATION_MATCH_WEIGHT * location_score

        # Experience match
        user_exp = user.experience or 0
        exp_min = job.experience_min or 0
        exp_max = job.experience_max or 99

        if exp_min <= user_exp <= exp_max:
            exp_score = 1.0
            reasons.append("experience_match")
        elif user_exp < exp_min:
            gap = exp_min - user_exp
            exp_score = max(0, 1 - (gap / 5))
        else:
            gap = user_exp - exp_max
            exp_score = max(0, 1 - (gap / 10))

        score += EXPERIENCE_MATCH_WEIGHT * exp_score

        # Popularity (placeholder — using recency as proxy)
        score += POPULARITY_WEIGHT * 0.5

        return score, reasons

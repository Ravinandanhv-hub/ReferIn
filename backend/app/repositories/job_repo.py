from sqlalchemy import String, select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.job import Job
from app.schemas.job import JobSearchParams


class JobRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, job_id: str) -> Job | None:
        result = await self.db.execute(select(Job).where(Job.id == job_id))
        return result.scalar_one_or_none()

    async def list_jobs(self, params: JobSearchParams) -> tuple[list[Job], int]:
        query = select(Job)
        count_query = select(func.count()).select_from(Job)

        # Full-text search using LIKE (SQLite compatible)
        if params.q:
            pattern = f"%{params.q}%"
            search_filter = or_(
                Job.title.ilike(pattern),
                Job.company.ilike(pattern),
                Job.description.ilike(pattern),
            )
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)

        # Filters
        if params.location:
            query = query.where(Job.location.ilike(f"%{params.location}%"))
            count_query = count_query.where(Job.location.ilike(f"%{params.location}%"))

        if params.type:
            query = query.where(Job.type == params.type)
            count_query = count_query.where(Job.type == params.type)

        if params.is_remote is not None:
            query = query.where(Job.is_remote == params.is_remote)
            count_query = count_query.where(Job.is_remote == params.is_remote)

        if params.experience_min is not None:
            query = query.where(Job.experience_max >= params.experience_min)
            count_query = count_query.where(Job.experience_max >= params.experience_min)

        if params.experience_max is not None:
            query = query.where(Job.experience_min <= params.experience_max)
            count_query = count_query.where(Job.experience_min <= params.experience_max)

        # Get total count
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # Pagination
        offset = (params.page - 1) * params.size
        query = query.order_by(Job.posted_at.desc()).offset(offset).limit(params.size)

        result = await self.db.execute(query)
        jobs = list(result.scalars().all())

        return jobs, total

    async def get_all_jobs(self) -> list[Job]:
        result = await self.db.execute(select(Job).order_by(Job.posted_at.desc()))
        return list(result.scalars().all())

    async def get_jobs_by_skills(self, skills: list[str], limit: int = 50) -> list[Job]:
        # SQLite: JSON column stored as text, use LIKE to match skills
        filters = []
        for skill in skills:
            filters.append(func.cast(Job.skills_required, String).ilike(f"%{skill}%"))
        if filters:
            query = select(Job).where(or_(*filters)).order_by(Job.posted_at.desc()).limit(limit)
        else:
            query = select(Job).order_by(Job.posted_at.desc()).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

import math
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.job_repo import JobRepository
from app.schemas.job import JobSearchParams, JobListResponse, JobResponse, JobDetailResponse


class JobService:
    def __init__(self, db: AsyncSession):
        self.repo = JobRepository(db)

    async def get_jobs(self, params: JobSearchParams) -> JobListResponse:
        jobs, total = await self.repo.list_jobs(params)
        pages = math.ceil(total / params.size) if total > 0 else 0

        return JobListResponse(
            items=[JobResponse.model_validate(j) for j in jobs],
            total=total,
            page=params.page,
            size=params.size,
            pages=pages,
        )

    async def get_job(self, job_id: str) -> JobDetailResponse:
        job = await self.repo.get_by_id(job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found",
            )
        return JobDetailResponse.model_validate(job)

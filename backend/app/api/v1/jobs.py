from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.job import (
    JobSearchParams,
    JobListResponse,
    JobDetailResponse,
    RecommendedJobListResponse,
)
from app.services.job_service import JobService
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("", response_model=JobListResponse)
async def list_jobs(
    q: str | None = None,
    location: str | None = None,
    type: str | None = None,
    is_remote: bool | None = None,
    experience_min: int | None = None,
    experience_max: int | None = None,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    params = JobSearchParams(
        q=q,
        location=location,
        type=type,
        is_remote=is_remote,
        experience_min=experience_min,
        experience_max=experience_max,
        page=page,
        size=size,
    )
    service = JobService(db)
    return await service.get_jobs(params)


@router.get("/recommended", response_model=RecommendedJobListResponse)
async def get_recommended_jobs(
    limit: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = RecommendationService(db)
    return await service.get_recommendations(current_user, limit)


@router.get("/{job_id}", response_model=JobDetailResponse)
async def get_job(job_id: str, db: AsyncSession = Depends(get_db)):
    service = JobService(db)
    return await service.get_job(job_id)

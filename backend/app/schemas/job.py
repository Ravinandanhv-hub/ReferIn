from pydantic import BaseModel, Field


class JobResponse(BaseModel):
    id: str
    title: str
    company: str
    location: str | None = None
    type: str
    skills_required: list[str] = []
    is_remote: bool = False
    experience_min: int = 0
    experience_max: int = 0
    posted_at: str
    source: str | None = None

    model_config = {"from_attributes": True}


class JobDetailResponse(JobResponse):
    description: str | None = None
    apply_url: str | None = None
    created_at: str


class JobListResponse(BaseModel):
    items: list[JobResponse]
    total: int
    page: int
    size: int
    pages: int


class JobSearchParams(BaseModel):
    q: str | None = None
    location: str | None = None
    type: str | None = None
    is_remote: bool | None = None
    experience_min: int | None = None
    experience_max: int | None = None
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)


class RecommendedJobResponse(JobResponse):
    score: float = 0.0
    match_reasons: list[str] = []


class RecommendedJobListResponse(BaseModel):
    items: list[RecommendedJobResponse]

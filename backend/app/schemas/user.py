from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    role: str = Field(default="job_seeker", pattern="^(job_seeker|referrer)$")


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    skills: list[str] = []
    experience: int = 0
    resume_url: str | None = None
    location: str | None = None
    preferences: dict = {}
    created_at: str

    model_config = {"from_attributes": True}


class UserPublicResponse(BaseModel):
    id: str
    name: str
    role: str
    skills: list[str] = []
    experience: int = 0
    location: str | None = None

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    skills: list[str] | None = None
    experience: int | None = Field(None, ge=0)
    location: str | None = None
    resume_url: str | None = None
    preferences: dict | None = None

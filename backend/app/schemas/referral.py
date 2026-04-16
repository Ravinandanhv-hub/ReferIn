from pydantic import BaseModel, Field


class ReferralCreate(BaseModel):
    job_id: str
    referrer_id: str
    message: str | None = Field(None, max_length=2000)


class ReferralUpdate(BaseModel):
    status: str = Field(..., pattern="^(accepted|rejected)$")


class ReferralResponse(BaseModel):
    id: str
    job_id: str
    requester_id: str
    referrer_id: str
    status: str
    message: str | None = None
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}


class ReferralListResponse(BaseModel):
    sent: list[ReferralResponse] = []
    received: list[ReferralResponse] = []

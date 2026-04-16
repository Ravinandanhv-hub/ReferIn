from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.referral import (
    ReferralCreate,
    ReferralUpdate,
    ReferralResponse,
    ReferralListResponse,
)
from app.services.referral_service import ReferralService

router = APIRouter(prefix="/referrals", tags=["Referrals"])


@router.post("", response_model=ReferralResponse, status_code=201)
async def create_referral(
    data: ReferralCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ReferralService(db)
    referral = await service.request_referral(current_user.id, data)
    return ReferralResponse.model_validate(referral)


@router.get("/my", response_model=ReferralListResponse)
async def get_my_referrals(
    status: str | None = Query(None, pattern="^(pending|accepted|rejected)$"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ReferralService(db)
    result = await service.get_my_referrals(current_user.id, status)
    return ReferralListResponse(
        sent=[ReferralResponse.model_validate(r) for r in result["sent"]],
        received=[ReferralResponse.model_validate(r) for r in result["received"]],
    )


@router.patch("/{referral_id}", response_model=ReferralResponse)
async def update_referral(
    referral_id: str,
    data: ReferralUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ReferralService(db)
    referral = await service.update_referral_status(
        referral_id, current_user.id, data.status
    )
    return ReferralResponse.model_validate(referral)

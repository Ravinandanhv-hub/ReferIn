from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.referral import Referral
from app.models.notification import Notification
from app.repositories.referral_repo import ReferralRepository
from app.repositories.notification_repo import NotificationRepository
from app.repositories.job_repo import JobRepository
from app.repositories.user_repo import UserRepository
from app.schemas.referral import ReferralCreate


class ReferralService:
    def __init__(self, db: AsyncSession):
        self.referral_repo = ReferralRepository(db)
        self.notification_repo = NotificationRepository(db)
        self.job_repo = JobRepository(db)
        self.user_repo = UserRepository(db)

    async def request_referral(
        self, requester_id: str, data: ReferralCreate
    ) -> Referral:
        # Validate no self-referral
        if requester_id == data.referrer_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot request referral from yourself",
            )

        # Validate job exists
        job = await self.job_repo.get_by_id(data.job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found",
            )

        # Validate referrer exists
        referrer = await self.user_repo.get_by_id(data.referrer_id)
        if not referrer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Referrer not found",
            )

        # Check for duplicate
        existing = await self.referral_repo.get_existing(
            data.job_id, requester_id, data.referrer_id
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Referral request already exists for this job and referrer",
            )

        # Create referral
        referral = Referral(
            job_id=data.job_id,
            requester_id=requester_id,
            referrer_id=data.referrer_id,
            message=data.message,
        )
        referral = await self.referral_repo.create(referral)

        # Get requester name for notification
        requester = await self.user_repo.get_by_id(requester_id)

        # Notify referrer
        notification = Notification(
            user_id=data.referrer_id,
            type="referral_request",
            title="New Referral Request",
            message=f"{requester.name} has requested a referral for {job.title} at {job.company}",
        )
        await self.notification_repo.create(notification)

        return referral

    async def get_my_referrals(
        self, user_id: str, status_filter: str | None = None
    ) -> dict:
        return await self.referral_repo.get_by_user(user_id, status=status_filter)

    async def update_referral_status(
        self, referral_id: str, user_id: str, new_status: str
    ) -> Referral:
        referral = await self.referral_repo.get_by_id(referral_id)
        if not referral:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Referral not found",
            )

        # Only referrer can accept/reject
        if referral.referrer_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the referrer can update the status",
            )

        if referral.status != "pending":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Referral is already {referral.status}",
            )

        updated = await self.referral_repo.update_status(referral_id, new_status)

        # Get job info for notification
        job = await self.job_repo.get_by_id(referral.job_id)
        referrer = await self.user_repo.get_by_id(user_id)

        # Notify requester
        notification = Notification(
            user_id=referral.requester_id,
            type=f"referral_{new_status}",
            title=f"Referral {new_status.capitalize()}",
            message=f"{referrer.name} has {new_status} your referral request for {job.title} at {job.company}",
        )
        await self.notification_repo.create(notification)

        return updated

from sqlalchemy import select, update, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.referral import Referral


class ReferralRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, referral: Referral) -> Referral:
        self.db.add(referral)
        await self.db.flush()
        await self.db.refresh(referral)
        return referral

    async def get_by_id(self, referral_id: str) -> Referral | None:
        result = await self.db.execute(
            select(Referral).where(Referral.id == referral_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user(
        self, user_id: str, role: str | None = None, status: str | None = None
    ) -> dict[str, list[Referral]]:
        sent_query = select(Referral).where(Referral.requester_id == user_id)
        received_query = select(Referral).where(Referral.referrer_id == user_id)

        if status:
            sent_query = sent_query.where(Referral.status == status)
            received_query = received_query.where(Referral.status == status)

        sent_query = sent_query.order_by(Referral.created_at.desc())
        received_query = received_query.order_by(Referral.created_at.desc())

        sent_result = await self.db.execute(sent_query)
        received_result = await self.db.execute(received_query)

        return {
            "sent": list(sent_result.scalars().all()),
            "received": list(received_result.scalars().all()),
        }

    async def get_existing(
        self, job_id: str, requester_id: str, referrer_id: str
    ) -> Referral | None:
        result = await self.db.execute(
            select(Referral).where(
                Referral.job_id == job_id,
                Referral.requester_id == requester_id,
                Referral.referrer_id == referrer_id,
            )
        )
        return result.scalar_one_or_none()

    async def update_status(self, referral_id: str, status: str) -> Referral | None:
        await self.db.execute(
            update(Referral)
            .where(Referral.id == referral_id)
            .values(status=status)
        )
        await self.db.flush()
        return await self.get_by_id(referral_id)

import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, ForeignKey, UniqueConstraint, CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


class Referral(Base):
    __tablename__ = "referrals"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    job_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False
    )
    requester_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    referrer_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(
        String(50), default=lambda: datetime.now(timezone.utc).isoformat()
    )
    updated_at: Mapped[str] = mapped_column(
        String(50),
        default=lambda: datetime.now(timezone.utc).isoformat(),
        onupdate=lambda: datetime.now(timezone.utc).isoformat(),
    )

    __table_args__ = (
        UniqueConstraint("job_id", "requester_id", "referrer_id", name="unique_referral"),
        CheckConstraint("requester_id != referrer_id", name="no_self_referral"),
        Index("idx_referrals_requester", "requester_id"),
        Index("idx_referrals_referrer", "referrer_id"),
        Index("idx_referrals_job", "job_id"),
        Index("idx_referrals_status", "status"),
    )

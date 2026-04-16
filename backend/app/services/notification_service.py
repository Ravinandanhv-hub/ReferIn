from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.notification_repo import NotificationRepository
from app.schemas.notification import NotificationListResponse, NotificationResponse
from fastapi import HTTPException, status


class NotificationService:
    def __init__(self, db: AsyncSession):
        self.repo = NotificationRepository(db)

    async def get_notifications(
        self, user_id: str, unread_only: bool = False
    ) -> NotificationListResponse:
        notifications = await self.repo.get_by_user(user_id, unread_only)
        return NotificationListResponse(
            items=[NotificationResponse.model_validate(n) for n in notifications]
        )

    async def mark_as_read(
        self, notification_id: str, user_id: str
    ) -> NotificationResponse:
        notification = await self.repo.mark_as_read(notification_id, user_id)
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found",
            )
        return NotificationResponse.model_validate(notification)

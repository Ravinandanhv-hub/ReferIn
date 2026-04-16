from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserPublicResponse, UserUpdate
from app.repositories.user_repo import UserRepository

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}", response_model=UserPublicResponse)
async def get_user_profile(
    user_id: str, db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)
    if not user:
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return UserPublicResponse.model_validate(user)


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = UserRepository(db)
    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        return UserResponse.model_validate(current_user)

    user = await repo.update(current_user.id, update_data)
    return UserResponse.model_validate(user)

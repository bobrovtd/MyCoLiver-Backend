from fastapi import APIRouter, Depends

from app.auth import fastapi_users, current_active_user
from app.models.users import User
from app.schemas import UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)


@router.get("/me/profile", response_model=UserRead)
async def get_user_profile(user: User = Depends(current_active_user)):
    """
    Get current user profile information
    """
    return user

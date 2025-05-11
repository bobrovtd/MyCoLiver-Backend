from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database.deps import get_async_session
from app.repositories.profile import UserProfileRepository
from app.schemas.profile import (
    UserProfileCreate,
    UserProfileResponse,
    UserProfileUpdate,
)

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.post("/", response_model=UserProfileResponse)
async def create_profile(
    profile_data: UserProfileCreate, session: AsyncSession = Depends(get_async_session)
):
    """
    Эндпоинт для создания профиля пользователя.
    """
    created_profile = await UserProfileRepository.create_user_profile(
        user_id=profile_data.id,
        profile_data=profile_data.model_dump(exclude_unset=True),
        session=session,
    )
    return created_profile


@router.get("/{user_id}", response_model=UserProfileResponse)
async def get_profile(user_id: str, session: AsyncSession = Depends(get_async_session)):
    """
    Эндпоинт для получения профиля пользователя по user_id.
    """
    profile = await UserProfileRepository.get_user_profile(
        user_id=user_id, session=session
    )
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.get("/", response_model=List[UserProfileResponse])
async def get_all_profiles(session: AsyncSession = Depends(get_async_session)):
    """
    Эндпоинт для получения всех профилей пользователей.
    """
    profiles = await UserProfileRepository.get_all_user_profiles(session=session)
    return profiles


@router.put("/{user_id}", response_model=UserProfileResponse)
async def update_profile(
    user_id: str,
    updated_data: UserProfileUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Эндпоинт для обновления профиля пользователя.
    """
    updated_profile = await UserProfileRepository.update_user_profile(
        user_id=user_id,
        updated_data=updated_data.model_dump(exclude_unset=True),
        session=session,
    )
    if not updated_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return updated_profile


@router.delete("/{user_id}")
async def delete_profile(
    user_id: str, session: AsyncSession = Depends(get_async_session)
):
    """
    Эндпоинт для удаления профиля пользователя.
    """
    success = await UserProfileRepository.delete_user_profile(
        user_id=user_id, session=session
    )
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"detail": "Profile deleted successfully"}

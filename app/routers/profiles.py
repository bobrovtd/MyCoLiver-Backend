from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from uuid import UUID

from app.auth.users import current_active_user
from app.database.deps import get_async_session
from app.models.users import User, UserProfile, UserImage
from app.schemas.users import UserProfileRead, UserProfileCreate, UserProfileUpdate, UserImageRead, \
    UserImageCreate

router = APIRouter()


@router.get("/me", response_model=UserProfileRead)
async def get_my_profile(
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Get the current user's profile"""
    stmt = select(UserProfile).where(UserProfile.user_id == user.id)
    result = await session.execute(stmt)
    profile = result.scalars().first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


@router.put("/me", response_model=UserProfileRead)
async def update_my_profile(
        profile_update: UserProfileUpdate,
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Update the current user's profile"""
    stmt = select(UserProfile).where(UserProfile.user_id == user.id)
    result = await session.execute(stmt)
    profile = result.scalars().first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Update profile fields
    for field, value in profile_update.dict(exclude_unset=True).items():
        setattr(profile, field, value)

    session.add(profile)
    await session.commit()
    await session.refresh(profile)

    return profile


@router.get("/images", response_model=List[UserImageRead])
async def get_my_images(
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Get the current user's images"""
    stmt = select(UserImage).where(UserImage.user_id == user.id)
    result = await session.execute(stmt)
    images = result.scalars().all()

    return images


@router.post("/images", response_model=UserImageRead)
async def add_image(
        image: UserImageCreate,
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Add a new image to the current user's profile"""
    # If this is set as primary, unset any existing primary images
    if image.is_primary:
        stmt = select(UserImage).where(
            UserImage.user_id == user.id,
            UserImage.is_primary == True
        )
        result = await session.execute(stmt)
        primary_images = result.scalars().all()

        for primary_image in primary_images:
            primary_image.is_primary = False
            session.add(primary_image)

    # Create new image
    db_image = UserImage(
        user_id=user.id,
        image_url=image.image_url,
        is_primary=image.is_primary
    )

    session.add(db_image)
    await session.commit()
    await session.refresh(db_image)

    return db_image


@router.delete("/images/{image_id}")
async def delete_image(
        image_id: UUID,
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Delete one of the current user's images"""
    stmt = select(UserImage).where(
        UserImage.id == image_id,
        UserImage.user_id == user.id
    )
    result = await session.execute(stmt)
    image = result.scalars().first()

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    await session.delete(image)
    await session.commit()

    return {"status": "success"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.database.deps import get_async_session
from app.repositories.ad import AdRepository
from app.schemas.ads import AdCreate, AdUpdate, AdResponse


router = APIRouter(prefix="/ads", tags=["Ads"])


@router.post("/", response_model=AdResponse)
async def create_ad(
    ad_data: AdCreate, session: AsyncSession = Depends(get_async_session)
):
    """
    Создать новое объявление.
    """
    new_ad = await AdRepository.create_ad(ad_data.dict(), session)
    return new_ad


@router.get("/{ad_id}", response_model=AdResponse)
async def get_ad(ad_id: UUID, session: AsyncSession = Depends(get_async_session)):
    """
    Получить объявление по ID.
    """
    ad = await AdRepository.get_ad_by_id(ad_id, session)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    return ad


@router.get("/", response_model=List[AdResponse])
async def get_all_ads(session: AsyncSession = Depends(get_async_session)):
    """
    Получить все объявления.
    """
    return await AdRepository.get_all_ads(session)


@router.get("/owner/{owner_id}", response_model=List[AdResponse])
async def get_ads_by_owner(
    owner_id: UUID, session: AsyncSession = Depends(get_async_session)
):
    """
    Получить все объявления, принадлежащие определенному владельцу.
    """
    return await AdRepository.get_ads_by_owner(owner_id, session)


@router.put("/{ad_id}", response_model=AdResponse)
async def update_ad(
    ad_id: UUID, ad_data: AdUpdate, session: AsyncSession = Depends(get_async_session)
):
    """
    Обновить объявление.
    """
    updated_ad = await AdRepository.update_ad(
        ad_id, ad_data.dict(exclude_unset=True), session
    )
    if not updated_ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    return updated_ad


@router.delete("/{ad_id}")
async def delete_ad(ad_id: UUID, session: AsyncSession = Depends(get_async_session)):
    """
    Удалить объявление.
    """
    is_deleted = await AdRepository.delete_ad(ad_id, session)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="Ad not found")
    return {"detail": "Ad deleted successfully"}

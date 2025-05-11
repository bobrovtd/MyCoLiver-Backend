from typing import List, Optional, Dict, Any
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.models.ads import Ad


class AdRepository:
    @staticmethod
    async def create_ad(ad_data: Dict[str, Any], session: AsyncSession) -> Ad:
        """
        Создает новое объявление.

        Args:
            ad_data: Словарь с данными объявления.
            session: Сессия для работы с базой данных.

        Returns:
            Созданное объявление.
        """
        new_ad = Ad(**ad_data)
        session.add(new_ad)
        await session.commit()
        await session.refresh(new_ad)
        return new_ad

    @staticmethod
    async def get_ad_by_id(ad_id: UUID, session: AsyncSession) -> Optional[Ad]:
        """
        Получает объявление по его ID.

        Args:
            ad_id: Идентификатор объявления.
            session: Сессия для работы с базой данных.

        Returns:
            Объект Ad или None, если не найдено.
        """
        stmt = select(Ad).where(Ad.ad_id == ad_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def get_ads_by_owner(owner_id: UUID, session: AsyncSession) -> List[Ad]:
        """
        Получает все объявления для определенного владельца.

        Args:
            owner_id: Идентификатор владельца.
            session: Сессия для работы с базой данных.

        Returns:
            Список объявлений владельца.
        """
        stmt = select(Ad).where(Ad.owner_id == owner_id)
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def update_ad(
        ad_id: UUID, updated_data: Dict[str, Any], session: AsyncSession
    ) -> Optional[Ad]:
        """
        Обновляет существующее объявление.

        Args:
            ad_id: Идентификатор объявления.
            updated_data: Словарь с обновленными данными.
            session: Сессия для работы с базой данных.

        Returns:
            Обновленное объявление или None, если не найдено.
        """
        stmt = update(Ad).where(Ad.ad_id == ad_id).values(**updated_data).returning(Ad)
        result = await session.execute(stmt)
        ad = result.scalars().first()
        if ad:
            await session.commit()
            await session.refresh(ad)
        return ad

    @staticmethod
    async def delete_ad(ad_id: UUID, session: AsyncSession) -> bool:
        """
        Удаляет объявление по его ID.

        Args:
            ad_id: Идентификатор объявления.
            session: Сессия для работы с базой данных.

        Returns:
            True, если объявление было удалено, иначе False.
        """
        stmt = delete(Ad).where(Ad.ad_id == ad_id)
        result = await session.execute(stmt)
        if result.rowcount > 0:
            await session.commit()
            return True
        return False

    @staticmethod
    async def get_all_ads(session: AsyncSession) -> List[Ad]:
        """
        Получает все объявления.

        Args:
            session: Сессия для работы с базой данных.

        Returns:
            Список всех объявлений.
        """
        stmt = select(Ad)
        result = await session.execute(stmt)
        return result.scalars().all()

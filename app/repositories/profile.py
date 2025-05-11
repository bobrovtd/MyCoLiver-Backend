from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Dict, Any
import uuid
from app.models.profiles import UserProfile


class UserProfileRepository:

    @staticmethod
    async def create_user_profile(
        user_id: str, profile_data: Dict[str, Any], session: AsyncSession
    ) -> UserProfile:
        """
        Создает новый профиль пользователя

        Args:
            user_id: идентификатор пользователя
            profile_data: данные профиля
            session: сессия базы данных

        Returns:
            Созданный профиль пользователя
        """
        new_profile = UserProfile(user_id=user_id, **profile_data)
        session.add(new_profile)
        await session.commit()
        await session.refresh(new_profile)
        return new_profile

    @staticmethod
    async def get_user_profile(
        user_id: str, session: AsyncSession
    ) -> UserProfile | None:
        """
        Получает профиль пользователя по его ID

        Args:
            user_id: идентификатор пользователя
            session: сессия базы данных

        Returns:
            Профиль пользователя или None, если профиль не найден
        """
        stmt = select(UserProfile).where(UserProfile.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def get_profile_by_id(
        profile_id: uuid.UUID, session: AsyncSession
    ) -> UserProfile | None:
        """
        Получает профиль по его ID (не по user_id)

        Args:
            profile_id: идентификатор профиля
            session: сессия базы данных

        Returns:
            Профиль пользователя или None, если профиль не найден
        """
        stmt = select(UserProfile).where(UserProfile.id == profile_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def get_all_user_profiles(session: AsyncSession) -> List[UserProfile]:
        """
        Получает все профили пользователей

        Args:
            session: сессия базы данных

        Returns:
            Список всех профилей пользователей
        """
        stmt = select(UserProfile)
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def update_user_profile(
        user_id: str, updated_data: Dict[str, Any], session: AsyncSession
    ) -> UserProfile | None:
        """
        Обновляет информацию профиля пользователя

        Args:
            user_id: идентификатор пользователя
            updated_data: обновленные данные профиля
            session: сессия базы данных

        Returns:
            Обновлённый профиль пользователя или None, если профиль не найден
        """
        profile = await UserProfileRepository.get_user_profile(user_id, session)
        if not profile:
            return None

        for key, value in updated_data.items():
            if hasattr(profile, key):
                setattr(profile, key, value)

        await session.commit()
        await session.refresh(profile)
        return profile

    @staticmethod
    async def delete_user_profile(user_id: str, session: AsyncSession) -> bool:
        """
        Удаляет профиль пользователя по его ID

        Args:
            user_id: идентификатор пользователя
            session: сессия базы данных

        Returns:
            True, если профиль был успешно удалён, иначе False
        """
        profile = await UserProfileRepository.get_user_profile(user_id, session)
        if not profile:
            return False

        await session.delete(profile)
        await session.commit()
        return True

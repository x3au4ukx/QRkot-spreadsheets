from dataclasses import dataclass
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation
from app.models.user import User


@dataclass
class CRUDBase:
    """Базовый CRUD класс для работы с моделями."""

    model: CharityProject | Donation

    async def get_multi(
        self,
        session: AsyncSession
    ):
        """Получить все объекты модели из БД."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None
    ):
        """Создать новый объект модели с привязкой к пользователю."""
        obj_in_data = obj_in.model_dump()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

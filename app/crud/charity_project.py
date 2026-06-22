from datetime import datetime, timedelta

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):
    """CRUD операции для модели CharityProject."""

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        """Получить проект по ID."""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ):
        """Обновить проект и закрыть при достижении full_amount."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        if db_obj.full_amount == db_obj.invested_amount:
            db_obj.fully_invested = True
            db_obj.close_date = datetime.now()
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
    ):
        """Удалить проект (установить close_date)."""
        db_obj.close_date = datetime.now()
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_id_by_name(
        self,
        obj_name: str,
        session: AsyncSession
    ):
        """Получить ID проекта по названию."""
        db_obj_id = await session.execute(
            select(self.model.id).where(
                self.model.name == obj_name
            )
        )
        return db_obj_id.scalars().first()

    async def get_projects_by_completion_rate(
        self,
        from_reserve: datetime,
        to_reserve: datetime,
        session: AsyncSession
    ):
        closed_projects = await session.execute(
            select(self.model).where(
                self.model.create_date >= from_reserve,
                self.model.close_date <= to_reserve
            )
        )
        return closed_projects.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
"""Объект CRUD для целевых проектов."""

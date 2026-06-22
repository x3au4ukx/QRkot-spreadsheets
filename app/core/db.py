from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, declared_attr, mapped_column
)

from app.core.config import settings


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy."""


class CommonMixin:
    """Миксин с общими полями для всех моделей."""

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_amount: Mapped[int] = mapped_column(Integer)
    invested_amount: Mapped[int] = mapped_column(Integer, default=0)
    fully_invested: Mapped[bool] = mapped_column(Boolean, default=False)
    create_date: Mapped[datetime] = mapped_column(DateTime,
                                                  default=datetime.now)
    close_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)


engine = create_async_engine(settings.database_url)
"""Асинхронный движок SQLAlchemy."""

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
"""Фабрика асинхронных сессий SQLAlchemy."""


async def get_async_session():
    """Генератор асинхронной сессии для внедрения зависимостей."""
    async with AsyncSessionLocal() as async_session:
        yield async_session

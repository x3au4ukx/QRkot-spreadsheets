import contextlib

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from app.core.config import settings
from app.core.db import get_async_session
from app.core.user import get_user_db, get_user_manager
from app.schemas.user import UserCreate


get_async_session_context = contextlib.asynccontextmanager(get_async_session)
"""Контекстный менеджер асинхронной сессии БД."""

get_user_db_context = contextlib.asynccontextmanager(get_user_db)
"""Контекстный менеджер для работы с пользователями в БД."""

get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)
"""Контекстный менеджер для управления пользователями."""


async def create_user(
        email: EmailStr, password: str, is_superuser: bool = False
):
    """Создать пользователя с указанными email, паролем и ролью."""
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser
                        )
                    )
    except UserAlreadyExists:
        pass


async def create_first_superuser():
    """Создать первого суперпользователя из настроек .env."""
    if (settings.first_superuser_email is not None
            and settings.first_superuser_password is not None):
        await create_user(
            email=settings.first_superuser_email,
            password=settings.first_superuser_password,
            is_superuser=True,
        )

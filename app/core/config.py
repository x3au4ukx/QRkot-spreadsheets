from typing import Optional

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения, загружаемые из .env файла."""

    app_title: str = 'Название проекта'
    description: str = 'Описание проекта'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    yandex_disk_token: Optional[str] = None
    report_format: str = "%Y.%m.%d %H:%M:%S"

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
"""Объект настроек приложения."""

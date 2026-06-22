from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, CommonMixin


LEN_NAME = 100
"""Максимальная длина названия проекта."""


class CharityProject(CommonMixin, Base):
    """Модель благотворительного проекта."""

    name: Mapped[str] = mapped_column(String(LEN_NAME), unique=True)
    description: Mapped[str] = mapped_column(String)

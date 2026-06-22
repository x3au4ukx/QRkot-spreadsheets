from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


MIN_LEN_NAME = 5
"""Минимальная длина названия проекта."""

MAX_LEN_NAME = 100
"""Максимальная длина названия проекта."""

MIN_LEN_DESCRIPTION = 10
"""Минимальная длина описания проекта."""

MIN_AMOUNT = 0
"""Минимальная сумма проекта (должна быть больше)."""


class CharityProjectBase(BaseModel):
    """Базовая схема благотворительного проекта с общими полями."""

    name: Optional[str] = Field(None, min_length=MIN_LEN_NAME,
                                max_length=MAX_LEN_NAME)
    description: Optional[str] = Field(None, min_length=MIN_LEN_DESCRIPTION)
    full_amount: Optional[int] = Field(None, gt=MIN_AMOUNT)

    model_config = ConfigDict(extra='forbid', from_attributes=True)

    @field_validator('name', 'description', 'full_amount')
    @classmethod
    def name_cannot_be_null(cls, value):
        """Проверить, что поля не равны None."""
        if value is None:
            error = 'Название, описание и сумма не может быть пустым!'
            raise ValueError(error)
        return value


class CharityProjectCreate(CharityProjectBase):
    """Схема для создания нового проекта (все поля обязательны)."""

    name: str = Field(..., min_length=MIN_LEN_NAME, max_length=MAX_LEN_NAME)
    description: str = Field(..., min_length=MIN_LEN_DESCRIPTION)
    full_amount: int = Field(..., gt=MIN_AMOUNT)


class CharityProjectDB(CharityProjectBase):
    """Схема проекта из БД (с вычисляемыми полями)."""

    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None


class CharityProjectUpdate(CharityProjectBase):
    """Схема для обновления проекта (все поля опциональны)."""

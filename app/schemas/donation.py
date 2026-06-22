from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


MIN_AMOUNT = 0
"""Минимальная сумма пожертвования (должна быть больше 0)."""


class DonationBase(BaseModel):
    """Базовая схема пожертвования."""

    full_amount: int = Field(..., gt=MIN_AMOUNT)
    comment: Optional[str] = None

    model_config = ConfigDict(extra='forbid', from_attributes=True)


class DonationCreate(DonationBase):
    """Схема для создания пожертвования."""


class DonationDB(DonationBase):
    """Схема пожертвования из БД (без инвестиционных полей)."""

    id: int
    create_date: datetime
    user_id: Optional[int] = None


class DonationFullInfoDB(DonationDB):
    """Полная схема пожертвования из БД (с инвестиционными полями)."""

    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime] = None
    user_id: Optional[int] = None


class DonationDBNotUserId(DonationBase):
    """Схема пожертвования из БД без user_id (для эндпоинта /my)."""

    id: int
    create_date: datetime

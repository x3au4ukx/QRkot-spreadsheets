from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import (
    DonationCreate, DonationDB, DonationDBNotUserId, DonationFullInfoDB
)
from app.services.investment_service import invest_donation_to_projects


router = APIRouter()
"""Роутер для работы с пожертвованиями."""

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
"""Зависимость с асинхронной сессией БД."""

CurrentUserDep = Annotated[User, Depends(current_user)]
"""Зависимость с текущим авторизованным пользователем."""


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={'user_id'}
)
async def create_donation(
    donation: DonationCreate,
    session: SessionDep,
    user: CurrentUserDep
):
    """
    Создать пожертвование.

    Только для зарегистрированных пользователей.
    """
    new_donation = await donation_crud.create(donation, session, user)
    await invest_donation_to_projects(new_donation, session)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(session: SessionDep):
    """
    Показать список всех пожертвований.

    Только для суперюзеров.
    """
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=list[DonationDBNotUserId],
    response_model_exclude_none=True,
    response_model_exclude={'user_id'}
)
async def get_user_donations(
    session: SessionDep,
    user: CurrentUserDep
):
    """
    Показать список пожертвований пользователя, выполняющего запрос.

    Только для зарегистрированных пользователей.
    """
    all_donations = await donation_crud.get_user_donations(session, user)
    return all_donations

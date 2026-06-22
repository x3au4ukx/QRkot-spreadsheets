from fastapi import APIRouter

from app.api.endpoints import (
    charity_project_router, donation_router, user_router, yandex_router
)


main_router = APIRouter()
"""Главный роутер приложения."""

main_router.include_router(
    charity_project_router,
    prefix='/charity_project',
    tags=['charity_projects']
)
main_router.include_router(
    donation_router,
    prefix='/donation',
    tags=['donations']
)
main_router.include_router(user_router)
main_router.include_router(
    yandex_router,
    prefix='/yandex',
    tags=['Yandex Disk']
)

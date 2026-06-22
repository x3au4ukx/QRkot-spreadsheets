from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.yandex_client import YandexDiskClient, get_yandex_client
from app.services.yandex_api import create_simple_report
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud


router = APIRouter()


@router.post(
    '/',
    response_model=str,
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        yandex_client: YandexDiskClient = Depends(get_yandex_client)
) -> str:
    """
    Создание отчёта в Excel-файле на Яндекс Диске
    """
    from_date = datetime(2000, 1, 1)
    to_date = datetime.now() + timedelta(days=365 * 100)
    projects = await charity_project_crud.get_projects_by_completion_rate(
        from_reserve=from_date,
        to_reserve=to_date,
        session=session
    )

    if not projects:
        raise HTTPException(
            status_code=404,
            detail="Нет данных для формирования отчёта"
        )

    try:
        upload_url = await create_simple_report(yandex_client, projects,
                                                'Reports')
        return upload_url
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при создании отчёта: {str(e)}"
        )

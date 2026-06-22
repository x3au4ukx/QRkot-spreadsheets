from datetime import datetime, timedelta
import io
from typing import List

import xlsxwriter

from app.core.yandex_client import YandexDiskClient
from app.models.charity_project import CharityProject
from app.core.config import settings


def format_time_delta(time: timedelta):
    hours = time.seconds // 3600
    minutes = (time.seconds % 3600) // 60
    if time.days > 0:
        return f'{time.days} дн. {hours} ч.'
    return f'{hours} ч. {minutes} мин.'


async def create_simple_report(
    yandex_client: YandexDiskClient,
    projects: List[CharityProject],
    folder: str = 'Reports'
) -> str:
    now_date_time = datetime.now().strftime(settings.report_format)
    safe_filename = f'QRKot_report_{now_date_time}'.replace(
        ':', '-').replace(' ', '_').replace('/', '-')
    upload_url, file_path = await yandex_client.create_excel_file(
        safe_filename, folder)
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet("Отчет")
    title_format = workbook.add_format({'bold': True, 'font_size': 14})
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#2F75B5',
        'font_color': 'white',
        'border': 1
    })
    cell_format = workbook.add_format({'border': 1, 'align': 'center'})
    total_cell_format = workbook.add_format({'bold': True, 'border': 1})
    worksheet.merge_range('A1:C1', f'Отчет от {now_date_time}', title_format)
    headers = ['Название проекта', 'Время сбора', 'Описание']
    for col, header in enumerate(headers):
        worksheet.write(1, col, header, header_format)
    for row, res in enumerate(projects, start=2):
        collection_time = res.close_date - res.create_date
        worksheet.write(row, 0, str(res.name), cell_format)
        worksheet.write(row, 1, format_time_delta(collection_time), cell_format)
        worksheet.write(row, 2, str(res.description), cell_format)
    last_cell = len(projects) + 2
    worksheet.merge_range(last_cell, 0, last_cell, 2,
                          f'Всего проектов: {len(projects)}',
                          total_cell_format)
    worksheet.set_column('A:A', 30)
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 30)
    workbook.close()
    output.seek(0)
    projects
    await yandex_client.upload_file(upload_url, output.getvalue())
    return await yandex_client.publish_file(file_path)

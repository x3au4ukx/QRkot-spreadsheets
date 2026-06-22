from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def invest_project_from_donations(
    new_project: CharityProject,
    session: AsyncSession
) -> None:
    """Инвестировать проект из доступных пожертвований."""
    available_donations = await session.execute(
        select(Donation).where(
            Donation.fully_invested.is_(False)
        )
    )
    available_donations = available_donations.scalars().all()
    if not available_donations:
        return
    for donation in available_donations:
        donation_invest_amount = (
            donation.full_amount - donation.invested_amount
        )
        project_invest_amount = (
            new_project.full_amount - new_project.invested_amount
        )
        invested_funds = min(donation_invest_amount, project_invest_amount)
        new_project.invested_amount += invested_funds
        donation.invested_amount += invested_funds
        if donation.invested_amount == donation.full_amount:
            donation.fully_invested = True
            donation.close_date = datetime.now()
        session.add(donation)
        if new_project.invested_amount == new_project.full_amount:
            new_project.fully_invested = True
            new_project.close_date = datetime.now()
            break
    session.add(new_project)
    await session.commit()


async def invest_donation_to_projects(
    new_donation: Donation,
    session: AsyncSession
):
    """Инвестировать пожертвование в доступные проекты."""
    available_projects = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested.is_(False)
        )
    )
    available_projects = available_projects.scalars().all()
    if not available_projects:
        return
    for project in available_projects:
        project_invest_amount = project.full_amount - project.invested_amount
        donation_invest_amount = (
            new_donation.full_amount - new_donation.invested_amount
        )
        invested_funds = min(project_invest_amount, donation_invest_amount)
        new_donation.invested_amount += invested_funds
        project.invested_amount += invested_funds
        if project.invested_amount == project.full_amount:
            project.fully_invested = True
            project.close_date = datetime.now()
        session.add(project)
        if new_donation.invested_amount == new_donation.full_amount:
            new_donation.fully_invested = True
            new_donation.close_date = datetime.now()
            break
    session.add(new_donation)
    await session.commit()

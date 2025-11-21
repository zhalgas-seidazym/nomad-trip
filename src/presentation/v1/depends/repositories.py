from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.companies.interfaces import ICompanyRepository
from src.application.companies.repositories import CompanyRepository
from src.application.users.interfaces import IUserRepository
from src.application.users.repositories import UserRepository
from src.domain.interfaces import IUoW
from src.presentation.v1.depends.session import get_session, get_uow


async def get_user_repository(
        session: AsyncSession = Depends(get_session),
        uow: IUoW = Depends(get_uow)
) -> IUserRepository:
    return UserRepository(session, uow)

async def get_company_repository(
        session: AsyncSession = Depends(get_session),
        uow: IUoW = Depends(get_uow)
) -> ICompanyRepository:
    return CompanyRepository(session, uow)
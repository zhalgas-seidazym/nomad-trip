from typing import Optional, Dict, Any, List

from sqlalchemy import select, or_, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.companies.dtos import CompanyDTO
from src.application.companies.interfaces import ICompanyRepository
from src.application.companies.models import Company
from src.domain.interfaces import IUoW


class CompanyRepository(ICompanyRepository):
    def __init__(self, session: AsyncSession, uow: IUoW):
        self._session = session
        self._uow = uow

    async def get_by_user_id(self, user_id: int) -> Optional[CompanyDTO]:
        query = select(Company).where(Company.owner_id == user_id)
        result = await self._session.execute(query)
        orm = result.scalar_one_or_none()
        return CompanyDTO().to_application(orm) if orm else None

    async def get_by_id(self, company_id: int) -> Optional[CompanyDTO]:
        query = select(Company).where(Company.id == company_id)
        result = await self._session.execute(query)
        orm = result.scalar_one_or_none()
        return CompanyDTO().to_application(orm) if orm else None

    async def get_by_name_or_description(self, text: str) -> Optional[List[CompanyDTO]]:
        query = select(Company).where(
            or_(
                Company.name.ilike(f"%{text}%"),
                Company.description.ilike(f"%{text}%")
            )
        )
        result = await self._session.execute(query)
        orm_list = result.scalars().all()
        return [CompanyDTO().to_application(orm) for orm in orm_list]

    async def add(self, company_data: Dict[str, Any]) -> Optional[CompanyDTO]:
        async with self._uow:
            query = insert(Company).values(**company_data).returning(Company)
            result = await self._session.execute(query)
            orm = result.scalar_one_or_none()
            return CompanyDTO().to_application(orm) if orm else None

    async def update(self, company_id: int, company_data: Dict[str, Any]) -> Optional[CompanyDTO]:
        if not company_data:
            return await self.get_by_id(company_id)

        async with self._uow:
            query = (
                update(Company)
                .where(Company.id == company_id)
                .values(**company_data)
                .returning(Company)
            )
            result = await self._session.execute(query)
            orm = result.scalar_one_or_none()
            return CompanyDTO.to_application(orm) if orm else None

    async def delete(self, company_id: int) -> Optional[CompanyDTO]:
        async with self._uow:
            query = delete(Company).where(Company.id == company_id).returning(Company.id)
            result = await self._session.execute(query)
            delete_id = result.scalar_one_or_none()
            return delete_id is not None
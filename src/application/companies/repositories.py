from typing import Optional, Dict, Any, List

from sqlalchemy import select, or_, insert, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.companies.dtos import CompanyDTO, PaginationCompanyDTO
from src.application.companies.interfaces import ICompanyRepository
from src.application.companies.models import Company
from src.domain.enums import Status
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

    async def get_by_query_and_status(
        self, text: str, pagination: Dict[str, Any], status: Optional[Status] = None
    ) -> PaginationCompanyDTO:

        page = pagination.get("page", 1)
        per_page = pagination.get("per_page", 10)

        conditions = [
            or_(
                Company.name.ilike(f"%{text}%"),
                Company.description.ilike(f"%{text}%")
            ),
        ]

        if status is not None:
            conditions.append(Company.status == status)

        count_query = select(func.count(Company.id)).where(*conditions)
        total = (await self._session.execute(count_query)).scalar_one()

        query = (
            select(Company)
            .where(*conditions)
            .offset((page - 1) * per_page)
            .limit(per_page)
        )

        result = await self._session.execute(query)
        orm_list = result.scalars().all()

        items = [CompanyDTO().to_application(orm) for orm in orm_list]

        return PaginationCompanyDTO(
            page=page,
            per_page=per_page,
            total=total,
            items=items
        )

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
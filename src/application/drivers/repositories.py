from fastapi import HTTPException, status
from sqlalchemy import select, insert, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.drivers.dtos import DriverDTO, PaginationDriverDTO, PaginationDriverCompanyDTO, DriverCompanyDTO
from src.application.drivers.interfaces import IDriverRepository, IDriverCompanyRepository
from src.application.drivers.models import Driver, driver_company_table
from src.domain.enums import Status
from typing import Dict, Any, Optional

from src.domain.interfaces import IUoW


class DriverRepository(IDriverRepository):
    def __init__(self, session: AsyncSession, uow: IUoW):
        self._session = session
        self._uow = uow

    async def get_by_user_id(self, user_id: int) -> Optional[DriverDTO]:
        query = select(Driver).where(Driver.user_id == user_id)
        result = await self._session.execute(query)
        orm = result.scalar_one_or_none()
        return DriverDTO().to_application(orm) if orm else None

    async def get_by_id(self, driver_id: int) -> Optional[DriverDTO]:
        query = select(Driver).where(Driver.id == driver_id)
        result = await self._session.execute(query)
        orm = result.scalar_one_or_none()
        return DriverDTO().to_application(orm) if orm else None

    async def get_by_status(self, status: Status, pagination: Dict[str, Any]) -> Optional[PaginationDriverDTO]:
        page = pagination.get("page", 1)
        per_page = pagination.get("per_page", 10)

        count_query = select(func.count(Driver.id)).where(Driver.status == status)
        total = (await self._session.execute(count_query)).scalar_one()

        query = select(Driver).where(Driver.status == status).offset((page - 1) * per_page).limit(per_page)
        result = await self._session.execute(query)
        orm_list = result.scalars().all()

        items = [DriverDTO().to_application(orm) for orm in orm_list]

        return PaginationDriverDTO(page=page, per_page=per_page, total=total, items=items)

    async def add(self, driver_data: Dict[str, Any]) -> Optional[DriverDTO]:
        async with self._uow:
            query = insert(Driver).values(**driver_data).returning(Driver)
            result = await self._session.execute(query)
            orm = result.scalar_one_or_none()
            return DriverDTO().to_application(orm) if orm else None

    async def update(self, driver_id: int, driver_data: Dict[str, Any]) -> Optional[DriverDTO]:
        if not driver_data:
            return await self.get_by_id(driver_id)

        async with self._uow:
            query = update(Driver).where(Driver.id == driver_id).values(**driver_data).returning(Driver)
            result = await self._session.execute(query)
            orm = result.scalar_one_or_none()
            return DriverDTO.to_application(orm) if orm else None

    async def delete(self, driver_id: int) -> Optional[bool]:
        async with self._uow:
            query = delete(Driver).where(Driver.id == driver_id).returning(Driver.id)
            result = await self._session.execute(query)
            delete_id = result.scalar_one_or_none()
            return delete_id is not None


class DriverCompanyRepository(IDriverCompanyRepository):
    def __init__(self, session: AsyncSession, uow: IUoW):
        self._session = session
        self._uow = uow

    async def get(
            self,
            driver_id: Optional[int],
            company_id: Optional[int],
            pagination: Dict[str, Any]
    ) -> PaginationDriverCompanyDTO:

        page = pagination.get("page", 1)
        per_page = pagination.get("per_page", 10)

        conditions = []

        if driver_id is not None:
            conditions.append(driver_company_table.c.driver_id == driver_id)

        if company_id is not None:
            conditions.append(driver_company_table.c.company_id == company_id)

        if not conditions:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")

        count_stmt = (
            select(func.count())
            .select_from(driver_company_table)
            .where(*conditions)
        )
        total = (await self._session.execute(count_stmt)).scalar_one()

        stmt = (
            select(driver_company_table)
            .where(*conditions)
            .offset((page - 1) * per_page)
            .limit(per_page)
        )

        result = await self._session.execute(stmt)
        rows = result.mappings().all()
        items = [DriverCompanyDTO(**row) for row in rows]

        return PaginationDriverCompanyDTO(
            page=page,
            per_page=per_page,
            total=total,
            items=items
        )
    async def add(self, driver_company_data: Dict[str, Any]) -> Optional[DriverCompanyDTO]:
        async with self._uow:
            stmt = insert(driver_company_table).values(**driver_company_data)
            await self._session.execute(stmt)
            return DriverCompanyDTO(**driver_company_data)

    async def update(
        self,
        driver_id: int,
        company_id: int,
        driver_company_data: Dict[str, Any]
    ) -> Optional[DriverCompanyDTO]:
        if not driver_company_data:
            paginated = await self.get(driver_id, company_id)
            return paginated.items[0] if paginated.items else None

        async with self._uow:
            stmt = (
                update(driver_company_table)
                .where(
                    driver_company_table.c.driver_id == driver_id,
                    driver_company_table.c.company_id == company_id
                )
                .values(**driver_company_data)
            )
            await self._session.execute(stmt)
            return DriverCompanyDTO(driver_id=driver_id, company_id=company_id, **driver_company_data)

    async def delete(self, driver_id: int, company_id: int) -> Optional[bool]:
        async with self._uow:
            stmt = delete(driver_company_table).where(
                driver_company_table.c.driver_id == driver_id,
                driver_company_table.c.company_id == company_id
            )
            result = await self._session.execute(stmt)
            return result.rowcount > 0

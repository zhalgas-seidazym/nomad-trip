from typing import Dict, Optional

from fastapi import HTTPException, status

from src.application.companies.dtos import CompanyDTO, PaginationCompanyDTO
from src.application.companies.interfaces import ICompanyController, ICompanyRepository, IAdminCompanyController
from src.application.users.dtos import UserDTO
from src.domain.enums import UserRoles, Status
from src.domain.interfaces import IStorageService


class CompanyController(ICompanyController):
    def __init__(
            self,
            company_repository: ICompanyRepository,
            storage_service: IStorageService,
    ):
        self._company_repository = company_repository
        self._storage_service = storage_service

    async def create_company(self, company_data: CompanyDTO) -> Dict:
        exists = await self._company_repository.get_by_user_id(company_data.owner_id)
        if exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already have a company")

        logo_url = await self._storage_service.upload_file(company_data.logo_file, 'logos')
        company_data.logo_url = logo_url
        company_data.logo_file = None

        created = await self._company_repository.add(company_data.to_payload(exclude_none=True))

        return {
            "detail": "Company created successfully",
            "company_id": created.id,
        }

    async def get_my_company(self, user_id: int) -> Dict:
        company = await self._company_repository.get_by_user_id(user_id)

        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not have a company")

        return company.to_payload(exclude_none=True)

    async def search_companies(self, user: UserDTO, text: str, company_status: Optional[Status], pagination: PaginationCompanyDTO) -> Dict:
        if not user.role == UserRoles.ADMIN:
            company_status = Status.APPROVED

        pagination_dto = await self._company_repository.get_by_query_and_status(
            text=text,
            status=company_status,
            pagination=pagination.to_payload(),
        )

        return pagination_dto.to_payload(exclude_none=True)

    async def get_company_by_id(self, user: UserDTO, company_id: int) -> Dict:
        company = await self._company_repository.get_by_id(company_id)

        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

        if not company.status == Status.APPROVED:
            if not user.role == UserRoles.ADMIN and not user.id == company.owner_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        return company.to_payload(exclude_none=True)

    async def update_company(self, user: UserDTO, company_data: CompanyDTO) -> Dict:
        company = await self._company_repository.get_by_user_id(user.id)

        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not have a company registered")

        if company_data.logo_file:
            logo_url = await self._storage_service.upload_file(company_data.logo_file, 'logos')
            company_data.logo_url = logo_url
            company_data.logo_file = None

            await self._storage_service.delete_file(company.logo_url)

        company_data.status = Status.WAITING

        company = await self._company_repository.update(company.id, company_data.to_payload(exclude_none=True))

        return company.to_payload(exclude_none=True)

    async def delete_company(self, user: UserDTO) -> Dict:
        company = await self._company_repository.get_by_user_id(user.id)

        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

        await self._company_repository.delete(company.id)

        return {
            "detail": "Company deleted successfully",
        }

class AdminCompanyController(IAdminCompanyController):
    ALLOWED_TRANSITIONS = {
        Status.WAITING: {Status.APPROVED, Status.REJECTED},
        Status.APPROVED: {Status.REJECTED},
        Status.REJECTED: {Status.APPROVED},
    }

    def __init__(
            self,
            company_repository: ICompanyRepository,
    ):
        self._company_repository = company_repository

    async def update_company_status(self, company_id: int, company_status: Status):
        company = await self._company_repository.get_by_id(company_id)

        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

        if not company_status in self.ALLOWED_TRANSITIONS.get(company.status):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot change status from {company.status} to {company_status}")

        await self._company_repository.update(company_id, CompanyDTO(status=company_status).to_payload(exclude_none=True))

        return {
            "detail": f"Company {company_id} status updated successfully",
        }


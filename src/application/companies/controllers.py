from typing import Dict, Optional

from fastapi import HTTPException, status

from src.application.companies.dtos import CompanyDTO, PaginationCompanyDTO
from src.application.companies.interfaces import ICompanyController, ICompanyRepository, IAdminCompanyController
from src.application.users.dtos import UserDTO
from src.application.users.interfaces import IUserRepository
from src.domain.enums import UserRoles, Status
from src.domain.interfaces import IStorageService
from src.domain.value_objects import ALLOWED_STATUS_TRANSITIONS, ALLOWED_IMAGE_TYPES


class CompanyController(ICompanyController):
    def __init__(
            self,
            company_repository: ICompanyRepository,
            user_repository: IUserRepository,
            storage_service: IStorageService,
    ):
        self._company_repository = company_repository
        self._user_repository = user_repository
        self._storage_service = storage_service

    async def create_company(self, user: UserDTO, company_data: CompanyDTO) -> Dict:
        if not user.role == UserRoles.PASSENGER:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User is not a PASSENGER. To change your role you should be passenger")

        exists = await self._company_repository.get_by_user_id(company_data.owner_id)
        if exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already have a company")

        if company_data.logo_file.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Incorrect image type")
        logo_url = await self._storage_service.upload_file(company_data.logo_file, 'logos')
        company_data.logo_url = logo_url
        company_data.logo_file = None

        created = await self._company_repository.add(company_data.to_payload(exclude_none=True))

        await self._user_repository.update(user_id=created.owner_id, user_data={"role": UserRoles.COMPANY})

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

        return company.to_payload(exclude_none=True)

    async def update_company(self, user: UserDTO, company_data: CompanyDTO) -> Dict:
        company = await self._company_repository.get_by_user_id(user.id)

        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not have a company registered")

        if company_data.logo_file:
            if company_data.logo_file.content_type not in ALLOWED_IMAGE_TYPES:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Incorrect image type")
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

        await self._storage_service.delete_file(company.logo_url)

        await self._company_repository.delete(company.id)

        await self._user_repository.update(user_id=user.id, user_data={"role": UserRoles.PASSENGER})

        return {
            "detail": "Company deleted successfully",
        }

class AdminCompanyController(IAdminCompanyController):
    def __init__(
            self,
            company_repository: ICompanyRepository,
    ):
        self._company_repository = company_repository

    async def update_company_status(self, company_data: CompanyDTO) -> Dict:
        company = await self._company_repository.get_by_id(company_data.id)

        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

        if not company_data.status in ALLOWED_STATUS_TRANSITIONS.get(company.status):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot change status from {company.status} to {company_data.status}")

        if company_data.status == Status.REJECTED and not company_data.rejection_reason:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot status to rejected without rejection reason")

        await self._company_repository.update(company_data.id, company_data.to_payload(exclude_none=True))

        return {
            "detail": f"Company {company_data.id} status updated successfully",
        }


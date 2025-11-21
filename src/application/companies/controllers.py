from typing import Dict

from fastapi import HTTPException, status

from src.application.companies.dtos import CompanyDTO
from src.application.companies.interfaces import ICompanyController, ICompanyRepository
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

    async def search_company(self, text: str) -> Dict: ...

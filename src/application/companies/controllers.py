from typing import Dict

from src.application.companies.dtos import CompanyDTO
from src.application.companies.interfaces import ICompanyController, ICompanyRepository


class CompanyController(ICompanyController):
    def __init__(
            self,
            company_repository: ICompanyRepository,
    ):
        self._company_repository = company_repository

    async def create_company(self, company_data: CompanyDTO) -> Dict: ...
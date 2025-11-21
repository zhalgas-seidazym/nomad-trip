from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

from src.application.companies.dtos import CompanyDTO


class ICompanyController(ABC):
    @abstractmethod
    async def create_company(self, company_data: CompanyDTO) -> Dict: ...

    @abstractmethod
    async def get_my_company(self, user_id: int) -> Dict: ...

    @abstractmethod
    async def search_company(self, text: str) -> Dict: ...

class ICompanyRepository(ABC):
    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> Optional[CompanyDTO]: ...

    @abstractmethod
    async def get_by_id(self, company_id: int) -> Optional[CompanyDTO]: ...

    @abstractmethod
    async def get_by_name_or_description(self, text: str, approved: bool) -> List[Optional[CompanyDTO]]: ...

    @abstractmethod
    async def get_by_status(self, status: str) -> List[Optional[CompanyDTO]]: ...

    @abstractmethod
    async def add(self, company_data: Dict[str, Any]) -> Optional[CompanyDTO]: ...

    @abstractmethod
    async def update(self, company_id: int, company_data: Dict[str, Any]) -> Optional[CompanyDTO]: ...

    @abstractmethod
    async def delete(self, company_id: int) -> Optional[CompanyDTO]: ...
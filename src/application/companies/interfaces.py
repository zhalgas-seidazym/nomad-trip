from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

from src.application.companies.dtos import CompanyDTO, PaginationCompanyDTO
from src.application.users.dtos import UserDTO
from src.domain.enums import Status

# TODO: get_applications, update_application_status

class ICompanyController(ABC):
    @abstractmethod
    async def create_company(self, user: UserDTO, company_data: CompanyDTO) -> Dict: ...

    @abstractmethod
    async def get_my_company(self, user_id: int) -> Dict: ...

    @abstractmethod
    async def search_companies(self, user: UserDTO, text: str, company_status: Optional[Status], pagination: PaginationCompanyDTO) -> Dict: ...

    @abstractmethod
    async def get_company_by_id(self, user: UserDTO, company_id: int) -> Dict: ...

    @abstractmethod
    async def update_company(self, user: UserDTO, company_data: CompanyDTO) -> Dict: ...

    @abstractmethod
    async def delete_company(self, user: UserDTO) -> Dict: ...

class IAdminCompanyController(ABC):
    @abstractmethod
    async def update_company_status(self, company_data: CompanyDTO) -> Dict: ...

class ICompanyRepository(ABC):
    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> Optional[CompanyDTO]: ...

    @abstractmethod
    async def get_by_id(self, company_id: int) -> Optional[CompanyDTO]: ...

    @abstractmethod
    async def get_by_query_and_status(self, text: str, status: str, pagination: Dict[str, Any]) -> PaginationCompanyDTO: ...

    @abstractmethod
    async def add(self, company_data: Dict[str, Any]) -> Optional[CompanyDTO]: ...

    @abstractmethod
    async def update(self, company_id: int, company_data: Dict[str, Any]) -> Optional[CompanyDTO]: ...

    @abstractmethod
    async def delete(self, company_id: int) -> Optional[bool]: ...
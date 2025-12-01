from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from src.application.drivers.dtos import DriverDTO, DriverCompanyDTO, PaginationDriverDTO, PaginationDriverCompanyDTO
from src.application.users.dtos import UserDTO
from src.domain.enums import Status

# TODO: update_driver_profile, get_driver_profile, get_driver_profile_by_id, delete_driver_profile, add_application, get_applications,
# TODO: update_driver_status

class IDriverController(ABC):
    @abstractmethod
    async def create_driver_profile(self, driver_data: DriverDTO, user: UserDTO)-> Dict: ...

class IDriverRepository(ABC):
    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> Optional[DriverDTO]: ...

    @abstractmethod
    async def get_by_id(self, driver_id: int) -> Optional[DriverDTO]: ...

    @abstractmethod
    async def get_by_status(self, status: Status, pagination: Dict[str, Any]) -> Optional[PaginationDriverDTO]: ...

    @abstractmethod
    async def add(self, driver_data: Dict[str, Any]) -> Optional[DriverDTO]: ...

    @abstractmethod
    async def update(self, driver_id: int, driver_data: Dict[str, Any]) -> Optional[DriverDTO]: ...

    @abstractmethod
    async def delete(self, driver_id: int) -> Optional[bool]: ...

class IDriverCompanyRepository(ABC):
    @abstractmethod
    async def get(self, driver_id: Optional[int], company_id: Optional[int], pagination: Dict[str, Any]) -> Optional[PaginationDriverCompanyDTO]: ...

    @abstractmethod
    async def add(self, driver_company_data: Dict[str, Any]) -> Optional[DriverCompanyDTO]: ...

    @abstractmethod
    async def update(
            self,
            driver_id: int,
            company_id: int,
            driver_company_data: Dict[str, Any]
    ) -> Optional[DriverCompanyDTO]: ...

    @abstractmethod
    async def delete(self, driver_id: int, company_id: int) -> Optional[bool]: ...
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from src.application.drivers.dtos import DriverDTO, DriverCompanyDTO, PaginationDriverDTO, PaginationDriverCompanyDTO
from src.application.users.dtos import UserDTO
from src.domain.enums import Status

# TODO: get_applications,
# TODO: update_driver_status, get_drivers_by_status

class IDriverController(ABC):
    @abstractmethod
    async def create_driver_profile(self, driver_data: DriverDTO, user: UserDTO) -> Dict: ...

    @abstractmethod
    async def get_my_driver_profile(self, user_id: int) -> Dict: ...

    @abstractmethod
    async def get_driver_profile_by_id(self, user: UserDTO, driver_id: int) -> Dict: ...

    @abstractmethod
    async def update_driver_profile(self, user: UserDTO, driver_data: DriverDTO) -> Dict: ...

    @abstractmethod
    async def delete_my_driver_profile(self, user: UserDTO) -> Dict: ...

    @abstractmethod
    async def add_application(self, user: UserDTO, company_id: int) -> Dict: ...

    @abstractmethod
    async def get_applications(self, user: UserDTO, application_status: Optional[Status], pagination: PaginationDriverCompanyDTO) -> Dict: ...

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
    async def get(
            self,
            driver_id: Optional[int],
            company_id: Optional[int],
            application_status: Optional[Status],
            pagination: Dict[str, Any]
    ) -> Optional[PaginationDriverCompanyDTO]: ...

    @abstractmethod
    async def get_by_id(self, driver_id: int, company_id: int) -> Optional[DriverCompanyDTO]: ...

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
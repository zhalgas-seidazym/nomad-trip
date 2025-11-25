from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from src.application.drivers.dtos import DriverDTO, DriverCompanyDTO, PaginationDriverDTO, PaginationDriverCompanyDTO
from src.domain.enums import Status


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
    async def get(self, driver_id: int, company_id: int, pagination: Dict[str, Any]) -> Optional[PaginationDriverCompanyDTO]: ...

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
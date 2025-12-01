from typing import Dict

from src.application.drivers.dtos import DriverDTO
from src.application.drivers.interfaces import IDriverController, IDriverRepository, IDriverCompanyRepository
from src.application.users.dtos import UserDTO
from src.domain.interfaces import IStorageService


class DriverController(IDriverController):
    def __init__(
            self,
            driver_repository: IDriverRepository,
            driver_company_repository: IDriverCompanyRepository,
            storage_service: IStorageService,
    ):
        self._driver_repository = driver_repository
        self._driver_company_repository = driver_company_repository
        self._storage_service = storage_service

    async def create_driver_profile(self, driver_data: DriverDTO, user: UserDTO) -> Dict:
        ...
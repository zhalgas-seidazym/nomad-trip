from typing import Dict

from fastapi import HTTPException, status

from src.application.drivers.dtos import DriverDTO
from src.application.drivers.interfaces import IDriverController, IDriverRepository, IDriverCompanyRepository
from src.application.users.dtos import UserDTO
from src.application.users.interfaces import IUserRepository
from src.domain.enums import UserRoles
from src.domain.interfaces import IStorageService
from src.domain.value_objects import ALLOWED_IMAGE_TYPES


class DriverController(IDriverController):
    def __init__(
            self,
            driver_repository: IDriverRepository,
            driver_company_repository: IDriverCompanyRepository,
            user_repository: IUserRepository,
            storage_service: IStorageService,
    ):
        self._driver_repository = driver_repository
        self._driver_company_repository = driver_company_repository
        self._user_repository = user_repository
        self._storage_service = storage_service

    async def create_driver_profile(self, driver_data: DriverDTO, user: UserDTO) -> Dict:
        if not user.role == UserRoles.PASSENGER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="To create a driver profile you must to be passenger")

        driver = await self._driver_repository.get_by_user_id(user.id)

        if driver:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Driver profile already exists")

        if driver_data.id_photo_file.content_type not in ALLOWED_IMAGE_TYPES or driver_data.licence_photo_file.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Incorrect image type")

        id_photo_url = await self._storage_service.upload_file(driver_data.id_photo_file, 'ids')
        driver_data.id_photo_url = id_photo_url
        driver_data.id_photo_file = None

        licence = await self._storage_service.upload_file(driver_data.licence_photo_file, 'ids')
        driver_data.licence = licence
        driver_data.licence_photo_file = None

        created = await self._driver_repository.add(driver_data.to_payload(exclude_none=True))

        await self._user_repository.update(user.id, {"role": UserRoles.DRIVER})

        return {
            "detail": "Driver profile created successfully",
            "driver_id": created.id,
        }

    async def get_my_driver_profile(self, user_id: int) -> Dict:
        driver_profile = await self._driver_repository.get_by_user_id(user_id)

        if not driver_profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver profile not found")

        return driver_profile.to_payload(exclude_none=True)

    async def get_driver_profile_by_id(self, user: UserDTO, driver_id: int) -> Dict:
        driver_profile = await self._driver_repository.get_by_id(driver_id)

        if not driver_profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver profile not found")

        if user.role == UserRoles.PASSENGER:
            driver_profile.id_photo_url = None
            driver_profile.license_photo_url = None

        if user.role == UserRoles.COMPANY:
            driver_profile.id_photo_url = None

        return driver_profile.to_payload(exclude_none=True)




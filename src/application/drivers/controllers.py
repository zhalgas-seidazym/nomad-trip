from datetime import datetime, timezone, timedelta
from typing import Dict

from fastapi import HTTPException, status

from src.application.companies.interfaces import ICompanyRepository
from src.application.drivers.dtos import DriverDTO, DriverCompanyDTO
from src.application.drivers.interfaces import IDriverController, IDriverRepository, IDriverCompanyRepository
from src.application.users.dtos import UserDTO
from src.application.users.interfaces import IUserRepository
from src.domain.enums import UserRoles, Status
from src.domain.interfaces import IStorageService
from src.domain.value_objects import ALLOWED_IMAGE_TYPES


class DriverController(IDriverController):
    def __init__(
            self,
            driver_repository: IDriverRepository,
            driver_company_repository: IDriverCompanyRepository,
            user_repository: IUserRepository,
            company_repository: ICompanyRepository,
            storage_service: IStorageService,
    ):
        self._driver_repository = driver_repository
        self._driver_company_repository = driver_company_repository
        self._user_repository = user_repository
        self._company_repository = company_repository
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

        license_photo_url = await self._storage_service.upload_file(driver_data.license_photo_file, 'licenses')
        driver_data.license_photo_url = license_photo_url
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

    async def update_driver_profile(self, user: UserDTO, driver_data: DriverDTO) -> Dict:
        driver_profile = await self._driver_repository.get_by_user_id(user.id)

        if not driver_profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver profile not found")

        if driver_data.id_photo_file:
            if driver_data.id_photo_file.content_type not in ALLOWED_IMAGE_TYPES:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Incorrect image type")
            id_photo_url = await self._storage_service.upload_file(driver_data.id_photo_file, 'ids')
            driver_data.id_photo_url = id_photo_url
            driver_data.id_photo_file = None

            await self._storage_service.delete_file(driver_profile.id_photo_url)

        if driver_data.license_photo_file:
            if driver_data.license_photo_file.content_type not in ALLOWED_IMAGE_TYPES:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Incorrect image type")
            license_photo_url = await self._storage_service.upload_file(driver_data.license_photo_file, 'ids')
            driver_data.license_photo_url = license_photo_url
            driver_data.license_photo_file = None

            await self._storage_service.delete_file(driver_profile.license_photo_url)


        driver_data.status = Status.WAITING

        updated = await self._driver_repository.update(driver_profile.id, driver_data.to_payload(exclude_none=True))

        return updated.to_payload(exclude_none=True)

    async def delete_my_driver_profile(self, user: UserDTO) -> Dict:
        driver_profile = await self._driver_repository.get_by_user_id(user.id)

        if not driver_profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver profile not found")

        await self._storage_service.delete_files([driver_profile.id_photo_url, driver_profile.license_photo_url])

        await self._driver_repository.delete(driver_profile.id)

        await self._user_repository.update(user_id=user.id, user_data={"role": UserRoles.PASSENGER})

        return {
            "detail": "Driver profile deleted successfully",
        }

    async def add_application(self, user: UserDTO, company_id: int) -> Dict:
        driver = await self._driver_repository.get_by_user_id(user.id)

        if not driver:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver profile not found")

        company = await self._company_repository.get_by_id(company_id)

        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

        application = await self._driver_company_repository.get_by_id(driver_id=driver.id, company_id=company_id)

        if application:
            now = datetime.now(timezone.utc)
            limit = application.updated_at + timedelta(days=30)

            if now < limit:
                remaining = limit - now
                days = remaining.days
                hours, remainder = divmod(remaining.seconds, 3600)
                minutes, _ = divmod(remainder, 60)

                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"You already applied to this company, try again in {days} days, {hours} hours, {minutes} minutes"
                )

            else:
                application.status = Status.WAITING
                application.rejection_reason = None

                await self._driver_company_repository.update(
                    driver_id=driver.id,
                    company_id=company_id,
                    driver_company_data=application.to_payload(exclude_none=True)
                )
        else:
            data = DriverCompanyDTO(
                driver_id=driver.id,
                company_id=company_id,
                status=Status.WAITING,
            )

            await self._driver_company_repository.add(data.to_payload(exclude_none=True))

        return {
            "detail": "Application added successfully",
        }





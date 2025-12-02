from dependency_injector.wiring import inject, Provide
from fastapi import Depends

from src.app.container import Container
from src.application.companies.controllers import CompanyController, AdminCompanyController
from src.application.companies.interfaces import ICompanyRepository, ICompanyController, IAdminCompanyController
from src.application.drivers.controllers import DriverController
from src.application.drivers.interfaces import IDriverRepository, IDriverCompanyRepository, IDriverController
from src.application.users.controllers import UserController
from src.application.users.interfaces import IUserRepository, IUserController, IEmailOtpService
from src.domain.interfaces import IJWTService, IHashService, IStorageService
from src.presentation.v1.depends.repositories import get_user_repository, get_company_repository, get_driver_repository, \
    get_driver_company_repository


@inject
async def get_user_controller(
        user_repository: IUserRepository = Depends(get_user_repository),
        email_otp_service: IEmailOtpService = Depends(Provide[Container.email_otp_service]),
        jwt_service: IJWTService = Depends(Provide[Container.jwt_service]),
        hash_service: IHashService = Depends(Provide[Container.hash_service]),
        storage_service: IStorageService = Depends(Provide[Container.minio_service]),
) -> IUserController:
    return UserController(
        user_repository=user_repository,
        email_otp_service=email_otp_service,
        jwt_service=jwt_service,
        hash_service=hash_service,
        storage_service=storage_service,
    )

@inject
async def get_company_controller(
        company_repository: ICompanyRepository = Depends(get_company_repository),
        user_repository: IUserRepository = Depends(get_user_repository),
        storage_service: IStorageService = Depends(Provide[Container.minio_service]),
) -> ICompanyController:
    return CompanyController(
        company_repository=company_repository,
        user_repository=user_repository,
        storage_service=storage_service,
    )

async def get_admin_company_controller(
        company_repository: ICompanyRepository = Depends(get_company_repository),
) -> IAdminCompanyController:
    return AdminCompanyController(
        company_repository=company_repository,
    )

async def get_driver_controller(
        driver_repository: IDriverRepository = Depends(get_driver_repository),
        driver_company_repository: IDriverCompanyRepository = Depends(get_driver_company_repository),
        user_repository: IUserRepository = Depends(get_user_repository),
        storage_service: IStorageService = Depends(Provide[Container.minio_service]),
) -> IDriverController:
    return DriverController(
        driver_repository=driver_repository,
        driver_company_repository=driver_company_repository,
        user_repository=user_repository,
        storage_service=storage_service,
    )
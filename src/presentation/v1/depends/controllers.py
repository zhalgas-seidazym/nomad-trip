from dependency_injector.wiring import inject, Provide
from fastapi import Depends

from src.app.container import Container
from src.application.companies.controllers import CompanyController, AdminCompanyController
from src.application.companies.interfaces import ICompanyRepository
from src.application.users.controllers import UserController
from src.application.users.interfaces import IUserRepository, IUserController, IEmailOtpService
from src.domain.interfaces import IJWTService, IHashService, IStorageService
from src.presentation.v1.depends.repositories import get_user_repository, get_company_repository


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
        storage_service: IStorageService = Depends(Provide[Container.minio_service]),
):
    return CompanyController(
        company_repository=company_repository,
        storage_service=storage_service,
    )

async def get_admin_company_controller(
        company_repository: ICompanyRepository = Depends(get_company_repository),
):
    return AdminCompanyController(
        company_repository=company_repository,
    )
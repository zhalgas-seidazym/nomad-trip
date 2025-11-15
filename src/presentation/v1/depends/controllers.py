from dependency_injector.wiring import inject, Provide
from fastapi import Depends

from src.app.container import container
from src.application.users.controllers import UserController
from src.application.users.interfaces import IUserRepository, IUserController, IEmailOtpService
from src.domain.interfaces import IJWTService, IHashService
from src.presentation.v1.depends.repositories import get_user_repository


@inject
async def get_user_controller(
        user_repository: IUserRepository = Depends(get_user_repository),
        email_otp_service: IEmailOtpService = Depends(Provide[container.email_otp_service]),
        jwt_service: IJWTService = Depends(Provide[container.jwt_service]),
        hash_service: IHashService = Depends(Provide[container.hash_service]),
) -> IUserController:
    return UserController(
        user_repository=user_repository,
        email_otp_service=email_otp_service,
        jwt_service=jwt_service,
        hash_service=hash_service,
    )
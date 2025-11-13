from dependency_injector.wiring import inject
from fastapi import Depends

from src.app.main import container
from src.application.users.controllers import UserController
from src.application.users.interfaces import IUserRepository, IUserController, IEmailOtpService
from src.infrastructure.integrations.jwt_service import JWTService
from src.presentation.v1.depends.repositories import get_user_repository


@inject
async def get_user_controller(
        user_repository: IUserRepository = Depends(get_user_repository),
        email_otp_service: IEmailOtpService = Depends(container.email_otp_service),
        jwt_service: JWTService = Depends(container.jwt_service)
) -> IUserController:
    return UserController(
        user_repository=user_repository,
        email_otp_service=email_otp_service,
        jwt_service=jwt_service
    )
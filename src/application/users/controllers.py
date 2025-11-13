from src.application.users.interfaces import IUserController, IUserRepository, IEmailOtpService
from src.domain.interfaces import IJWTService


class UserController(IUserController):
    def __init__(
            self,
            user_repository: IUserRepository,
            email_otp_service: IEmailOtpService,
            jwt_service: IJWTService,
    ):
        ...
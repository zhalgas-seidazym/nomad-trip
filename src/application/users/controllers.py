from fastapi import HTTPException, status
from starlette.responses import Response

from src.application.users.dtos import UserDTO
from src.application.users.interfaces import IUserController, IUserRepository, IEmailOtpService
from src.domain.interfaces import IJWTService


class UserController(IUserController):
    def __init__(
            self,
            user_repository: IUserRepository,
            email_otp_service: IEmailOtpService,
            jwt_service: IJWTService,
    ):
        self.user_repository = user_repository
        self.email_otp_service = email_otp_service
        self.jwt_service = jwt_service

    async def send_otp(self, user: UserDTO):
        user_check = await self.user_repository.get_by_email(user.email)
        if user_check is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with {user.email} already exists")
        await self.email_otp_service.send_otp(user.email)
        return {
            "detail": "OTP code sent successfully",
        }

    async def verify_otp(self, user: UserDTO, code: str, response: Response):
        await self.email_otp_service.verify_otp(user.email, code)

        created = await self.user_repository.add(user.to_payload(exclude_none=True))

        payload = {
            "user_id": created.id,
        }

        access_token = self.jwt_service.create_token(data=payload)
        refresh_token = self.jwt_service.create_token(data=payload, is_access_token=False)

        response.set_cookie(key="access_token", value=access_token, httponly=True)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

        return {
            "details": "OTP verified and user created successfully",
            "user_id": created.id,
        }

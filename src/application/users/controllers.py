from fastapi import HTTPException, status
from starlette.responses import Response

from src.application.users.dtos import UserDTO
from src.application.users.interfaces import IUserController, IUserRepository, IEmailOtpService
from src.domain.enums import UserRoles
from src.domain.interfaces import IJWTService, IHashService


class UserController(IUserController):
    def __init__(
            self,
            user_repository: IUserRepository,
            email_otp_service: IEmailOtpService,
            jwt_service: IJWTService,
            hash_service: IHashService,
    ):
        self.user_repository = user_repository
        self.email_otp_service = email_otp_service
        self.jwt_service = jwt_service
        self.hash_service = hash_service

    async def send_otp(self, user_data: UserDTO):
        user_check = await self.user_repository.get_by_email(user_data.email)
        if user_check is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with {user_data.email} already exists")
        await self.email_otp_service.send_otp(user_data.email)
        return {
            "detail": "OTP code sent successfully",
        }

    async def verify_otp(self, user_data: UserDTO, code: str, response: Response):
        await self.email_otp_service.verify_otp(user_data.email, code)

        user_data.password = self.hash_service.hash_password(user_data.password)

        created = await self.user_repository.add(user_data.to_payload(exclude_none=True))

        payload = {
            "user_id": created.id,
        }

        access_token = self.jwt_service.encode_token(data=payload)
        refresh_token = self.jwt_service.encode_token(data=payload, is_access_token=False)

        response.set_cookie(key="access_token", value=access_token, httponly=True)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

        return {
            "details": "OTP verified and user created successfully",
            "user_id": created.id,
        }

    async def login(self, user_data: UserDTO, response: Response):
        user = await self.user_repository.get_by_email(user_data.email)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {user_data.email} not found")

        password_check = self.hash_service.verify_password(user_data.password, user.password)

        if not password_check:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Incorrect credentials")

        payload = {
            "user_id": user.id,
        }

        access_token = self.jwt_service.encode_token(data=payload)
        refresh_token = self.jwt_service.encode_token(data=payload, is_access_token=False)

        response.set_cookie(key="access_token", value=access_token, httponly=True)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

        return {
            "details": "Logged in successfully",
        }

    # async def get_profile(self, user_id: int):
    #     user = await self.user_repository.get_by_id(user_id)
    #
    #     if user is None:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {user_id} id not found")
    #
    #     if user.role == UserRoles.ADMIN:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Access denied")
    #
    #     user.password = None
    #
    #     return user.to_payload(exclude_none=True)
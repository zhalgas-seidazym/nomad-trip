from typing import Annotated

from fastapi import APIRouter, status, Depends, Response

from src.application.users.dtos import UserDTO
from src.application.users.interfaces import IUserController
from src.domain.responses import RESPONSE_404, RESPONSE_401, RESPONSE_403
from src.presentation.v1.depends.controllers import get_user_controller
from src.presentation.v1.depends.security import get_current_user
from src.presentation.v1.schemas.user_schema import SendOTPSchema, VerifyOTPSchema, LoginSchema, UserSchema, \
    UpdateUserSchema

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.post(
    "/send-otp",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "OTP code sent",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "OTP code sent successfully"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Request cannot be processed. Possible reasons: user already exists, or OTP was already sent and has not expired yet.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User already exists"
                    }
                }
            }
        }
    }
)
async def send_otp(
        body: SendOTPSchema,
        controller: Annotated[IUserController, Depends(get_user_controller)],
):
    return await controller.send_otp(UserDTO(email=body.dict().get("email")))

@router.post(
    '/verify-otp',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "User created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "OTP code verified and user created successfully",
                        "user_id": 1
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Incorrect or expired otp code",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Incorrect or expired otp code"
                    }
                }
            }
        }
    }
)
async def verify_otp(
        body: VerifyOTPSchema,
        response: Response,
        controller: Annotated[IUserController, Depends(get_user_controller)],
):
    return await controller.verify_otp(
        user_data = UserDTO(**body.dict()), code=body.code, response=response
    )

@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Logged in successfully",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Logged in successfully"
                    }
                }
            }
        },
        status.HTTP_404_NOT_FOUND: RESPONSE_404,
        status.HTTP_400_BAD_REQUEST: {
            "description": "Incorrect credentials",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Incorrect credentials"
                    }
                }
            }
        }
    }
)
async def login(
    body: LoginSchema,
    response: Response,
    controller: Annotated[IUserController, Depends(get_user_controller)],
):
    return await controller.login(user_data=UserDTO(**body.dict()), response=response)

@router.get(
    '/profile',
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
    responses={
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401
    }
)
async def my_profile(
        user: UserDTO = Depends(get_current_user)
):
    user.password = None
    return user.to_payload(exclude_none=True)

@router.get(
    '/profile/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
    responses={
        status.HTTP_403_FORBIDDEN: RESPONSE_403,
        status.HTTP_404_NOT_FOUND: RESPONSE_404,
    }
)
async def profile_by_id(
        user_id: int,
        controller: Annotated[IUserController, Depends(get_user_controller)],
):
    return controller.get_profile(user_id=user_id)

@router.put(
    '/profile',
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
    responses={
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    }
)
async def update_profile(
        body: UpdateUserSchema,
        controller: Annotated[IUserController, Depends(get_user_controller)],
        user: UserDTO = Depends(get_current_user),
):
    return await controller.update(user=user, user_data=UserDTO(**body.dict()))
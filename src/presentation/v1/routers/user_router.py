from typing import Annotated

from fastapi import APIRouter, status, Depends, Response

from src.application.users.dtos import UserDTO
from src.application.users.interfaces import IUserController
from src.presentation.v1.depends.controllers import get_user_controller
from src.presentation.v1.schemas.user_schema import SendOTPSchema, VerifyOTPSchema

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
    return await controller.send_otp(UserDTO(email=body.email))

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
        user = UserDTO(**body), code=body.code, response=response
    )
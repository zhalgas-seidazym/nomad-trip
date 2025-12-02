from typing import Annotated

from fastapi import APIRouter, status, Depends, UploadFile, File

from src.application.drivers.dtos import DriverDTO
from src.application.drivers.interfaces import IDriverController
from src.application.users.dtos import UserDTO
from src.domain.responses import *
from src.presentation.v1.depends.controllers import get_driver_controller
from src.presentation.v1.depends.security import is_driver, get_current_user
from src.presentation.v1.schemas.driver_schema import CreateDriverSchema, DriverSchema

router = APIRouter(
    prefix="/driver",
    tags=["driver"]
)

admin_router = APIRouter(
    prefix="/driver",
    tags=["admin", "driver"]
)

@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Driver profile created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Driver profile created successfully, please wait until confirmation",
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: RESPONSE_400,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
        status.HTTP_403_FORBIDDEN: RESPONSE_403,
        status.HTTP_409_CONFLICT: RESPONSE_409,
    }
)
async def create_driver_profile(
        controller: Annotated[IDriverController, Depends(get_driver_controller)],
        licence_photo_file: UploadFile = File(),
        id_photo_file: UploadFile = File(),
        body: CreateDriverSchema = Depends(CreateDriverSchema.as_form()),
        user: UserDTO = Depends(get_current_user),
):
    return await controller.create_driver_profile(
        user=user,
        driver_data=DriverDTO(
            **body.dict(),
            user_id=user.id,
            id_photo_file=id_photo_file,
            licence_photo_file=licence_photo_file
        )
    )

@router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=DriverSchema,
    responses={
        status.HTTP_403_FORBIDDEN: RESPONSE_403,
        status.HTTP_404_NOT_FOUND: RESPONSE_404,
    }
)
async def get_my_driver_profile(
        controller: Annotated[IDriverController, Depends(get_driver_controller)],
        user: UserDTO = Depends(is_driver),
):
    return await controller.get_my_driver_profile(user_id=user.id)
from typing import Annotated, Optional

from fastapi import APIRouter, status, Depends, UploadFile, File, Body, Query

from src.application.drivers.dtos import DriverDTO, PaginationDriverCompanyDTO
from src.application.drivers.interfaces import IDriverController
from src.application.users.dtos import UserDTO
from src.domain.base_schema import PaginationSchema
from src.domain.enums import Status
from src.domain.responses import *
from src.presentation.v1.depends.controllers import get_driver_controller
from src.presentation.v1.depends.security import is_driver, get_current_user
from src.presentation.v1.schemas.driver_schema import CreateDriverSchema, DriverSchema, UpdateDriverSchema, \
    PaginationDriverCompanySchema

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
                        "driver_id": 1
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
        license_photo_file: UploadFile = File(),
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
            license_photo_file=license_photo_file
        )
    )

@router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=DriverSchema,
    responses={
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
        status.HTTP_403_FORBIDDEN: RESPONSE_403,
        status.HTTP_404_NOT_FOUND: RESPONSE_404,
    }
)
async def get_my_driver_profile(
        controller: Annotated[IDriverController, Depends(get_driver_controller)],
        user: UserDTO = Depends(is_driver),
):
    return await controller.get_my_driver_profile(user_id=user.id)

@router.post(
    '/application',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Application created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Application created successfully, please wait until confirmation",
                    }
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
        status.HTTP_403_FORBIDDEN: RESPONSE_403,
        status.HTTP_404_NOT_FOUND: RESPONSE_404,
        status.HTTP_409_CONFLICT: RESPONSE_409,
    }
)
async def add_application(
        controller: Annotated[IDriverController, Depends(get_driver_controller)],
        company_id: int = Body(),
        user: UserDTO = Depends(is_driver),
):
    return await controller.add_application(user, company_id)

@router.get(
    '/application',
    status_code=status.HTTP_200_OK,
    response_model=PaginationDriverCompanySchema,
    responses={
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
        status.HTTP_403_FORBIDDEN: RESPONSE_403,
        status.HTTP_404_NOT_FOUND: RESPONSE_404,
    }
)
async def get_my_applications(
        controller: Annotated[IDriverController, Depends(get_driver_controller)],
        application_status: Optional[Status] = Query(None),
        pagination: PaginationDriverCompanySchema = Depends(PaginationSchema.as_query()),
        user: UserDTO = Depends(is_driver),
):
    return await controller.get_applications(user=user, application_status=application_status, pagination=PaginationDriverCompanyDTO(**pagination.dict()))


@router.get(
    '/{driver_id}',
    status_code=status.HTTP_200_OK,
    response_model=DriverSchema,
    responses={
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
        status.HTTP_404_NOT_FOUND: RESPONSE_404,
    }
)
async def get_driver_profile_by_id(
        driver_id: int,
        controller: Annotated[IDriverController, Depends(get_driver_controller)],
        user: UserDTO = Depends(get_current_user),
):
    return await controller.get_driver_profile_by_id(user=user, driver_id=driver_id)

@router.put(
    '',
    status_code=status.HTTP_200_OK,
    response_model=DriverSchema,
    responses={
        status.HTTP_400_BAD_REQUEST: RESPONSE_400,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
        status.HTTP_403_FORBIDDEN: RESPONSE_403,
        status.HTTP_404_NOT_FOUND: RESPONSE_404,
    }
)
async def update_driver_profile(
        controller: Annotated[IDriverController, Depends(get_driver_controller)],
        license_photo_file: UploadFile = File(None),
        id_photo_file: UploadFile = File(None),
        body: UpdateDriverSchema = Depends(UpdateDriverSchema.as_form()),
        user: UserDTO = Depends(is_driver),
):
    return await controller.update_driver_profile(user, DriverDTO(
        **body.dict(),
        license_photo_file=license_photo_file,
        id_photo_file=id_photo_file
    ))

@router.delete(
    '',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Driver profile deleted successfully",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Driver profile deleted successfully",
                    }
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
        status.HTTP_403_FORBIDDEN: RESPONSE_403,
        status.HTTP_404_NOT_FOUND: RESPONSE_404,
    }
)
async def delete_my_driver_profile(
        controller: Annotated[IDriverController, Depends(get_driver_controller)],
        user: UserDTO = Depends(is_driver),
):
    return await controller.delete_my_driver_profile(user=user)
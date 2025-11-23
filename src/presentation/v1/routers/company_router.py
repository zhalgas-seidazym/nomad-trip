from typing import Annotated, Optional

from fastapi import APIRouter, status, Depends, UploadFile, File, Query, Body

from src.application.companies.dtos import CompanyDTO, PaginationCompanyDTO
from src.application.companies.interfaces import ICompanyController, IAdminCompanyController
from src.application.users.dtos import UserDTO
from src.domain.enums import Status
from src.domain.responses import *
from src.presentation.v1.depends.controllers import get_company_controller, get_admin_company_controller
from src.presentation.v1.depends.security import get_current_user, is_admin
from src.presentation.v1.schemas.company_schema import CreateCompanySchema, CompanySchema, PaginationCompanySchema, \
    UpdateCompanySchema

router = APIRouter(
    prefix="/company",
    tags=["company"]
)
admin_router = APIRouter(
    prefix="/company",
    tags=["admin", "company"]
)

@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Company created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Company created successfully, please wait until confirmation",
                    }
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
        status.HTTP_409_CONFLICT: RESPONSE_409
    }
)
async def create_company(
        controller: Annotated[ICompanyController, Depends(get_company_controller)],
        logo: UploadFile = File(),
        body: CreateCompanySchema = Depends(CreateCompanySchema.as_form()),
        user: UserDTO = Depends(get_current_user),
):
    return await controller.create_company(CompanyDTO(**body.dict(), owner_id=user.id, logo_file=logo))

@router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=CompanySchema,
    responses={
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
        status.HTTP_404_NOT_FOUND: RESPONSE_404,
    }
)
async def get_my_company(
        controller: Annotated[ICompanyController, Depends(get_company_controller)],
        user: UserDTO = Depends(get_current_user),
):
    return await controller.get_my_company(user.id)

@router.get(
    '/search',
    status_code=status.HTTP_200_OK,
    response_model=PaginationCompanySchema,
    responses={
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    }
)
async def search_companies(
        controller: Annotated[ICompanyController, Depends(get_company_controller)],
        user: UserDTO = Depends(get_current_user),
        query: str = Query(''),
        company_status: Optional[Status] = Query(None),
        pagination: PaginationCompanySchema = Depends(PaginationCompanySchema.as_query()),
):
    return await controller.search_companies(user=user, text=query, company_status=company_status, pagination=PaginationCompanyDTO(**pagination.dict()))

@router.get(
    '/{company_id}',
    status_code=status.HTTP_200_OK,
    response_model=CompanySchema,
    responses={
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
        status.HTTP_404_NOT_FOUND: RESPONSE_404,
        status.HTTP_403_FORBIDDEN: RESPONSE_403,
    }
)
async def get_company_by_id(
        company_id: int,
        controller: Annotated[ICompanyController, Depends(get_company_controller)],
        user: UserDTO = Depends(get_current_user),
):
    return await controller.get_company_by_id(company_id=company_id, user=user)

@router.put(
    '',
    status_code=status.HTTP_200_OK,
    response_model=CompanySchema,
    responses={
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
        status.HTTP_404_NOT_FOUND: RESPONSE_404,
    }
)
async def update_company(
        controller: Annotated[ICompanyController, Depends(get_company_controller)],
        logo_file: UploadFile = File(None),
        body: UpdateCompanySchema = Depends(UpdateCompanySchema.as_form()),
        user: UserDTO = Depends(get_current_user),
):
    return await controller.update_company(user, CompanyDTO(**body.dict(), logo_file=logo_file))

@admin_router.patch(
    '/{company_id}',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Company status updated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Company status updated successfully",
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: RESPONSE_400,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
        status.HTTP_403_FORBIDDEN: RESPONSE_403,
        status.HTTP_404_NOT_FOUND: RESPONSE_404,
    }
)
async def update_company_status(
        controller: Annotated[IAdminCompanyController, Depends(get_admin_company_controller)],
        company_id: int,
        company_status: Status = Body(),
        user: UserDTO = Depends(is_admin),
):
    return await controller.update_company_status(company_id=company_id, company_status=company_status)
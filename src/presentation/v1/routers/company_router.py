from fastapi import APIRouter, status

from src.domain.responses import *

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

): ...
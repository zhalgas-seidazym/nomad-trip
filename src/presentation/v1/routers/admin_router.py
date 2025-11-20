from fastapi import APIRouter

from . import company_router

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

router.include_router(company_router.admin_router)
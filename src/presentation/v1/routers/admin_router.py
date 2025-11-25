from fastapi import APIRouter

from . import company_router, driver_router

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

router.include_router(company_router.admin_router)
router.include_router(driver_router.admin_router)
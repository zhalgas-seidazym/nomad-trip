from fastapi import APIRouter


router = APIRouter(
    prefix="/driver",
    tags=["driver"]
)

admin_router = APIRouter(
    prefix="/driver",
    tags=["admin", "driver"]
)
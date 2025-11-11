from fastapi import APIRouter, status

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# @router.post("/get-otp")
# def get_otp()
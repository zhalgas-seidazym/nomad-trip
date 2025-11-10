from fastapi import APIRouter, status

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

# @router.post("/get-otp")
# def get_otp()
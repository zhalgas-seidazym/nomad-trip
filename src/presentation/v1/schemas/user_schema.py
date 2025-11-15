from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, field_validator

from src.domain.enums import UserRoles


class SendOTPSchema(BaseModel):
    email: EmailStr

class VerifyOTPSchema(BaseModel):
    email: EmailStr
    password: str
    password2: str
    first_name: str
    last_name: Optional[str] = None
    is_company: Optional[bool] = False
    code: str

    @field_validator("password2")
    def passwords_match(cls, v, values):
        password = values.get("password")
        if password != v:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
        return v

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: Optional[str] = None
    role: Optional[UserRoles] = None

    class Config:
        use_enum_values = True

# class UpdateUserSchema(BaseModel):
#     email: Optional[EmailStr] = None
#     first_name: Optional[str] = None
#     last_name: Optional[str] = None

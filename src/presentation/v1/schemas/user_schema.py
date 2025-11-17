from typing import Optional

from pydantic import BaseModel, EmailStr

from src.domain.enums import UserRoles


class SendOTPSchema(BaseModel):
    email: EmailStr

class VerifyOTPSchema(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: Optional[str] = None
    is_company: Optional[bool] = False
    code: str

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

class UpdateUserSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    new_password: Optional[str] = None

class RefreshTokenSchema(BaseModel):
    token: str

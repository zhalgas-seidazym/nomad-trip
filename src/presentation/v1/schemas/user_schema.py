from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from src.domain.base_schema import BaseSchema
from src.domain.enums import UserRoles


class VerifyOTPSchema(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    code: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRoles
    avatar_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        use_enum_values = True

class UpdateUserSchema(BaseSchema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    new_password: Optional[str] = None
    avatar_url: Optional[str] = None
from typing import Optional

from pydantic import BaseModel, EmailStr


class SendOTPSchema(BaseModel):
    email: EmailStr

class VerifyOTPSchema(BaseModel):
    email: EmailStr
    password: str
    password2: str
    first_name: str
    last_name: Optional[str] = None
    code: str
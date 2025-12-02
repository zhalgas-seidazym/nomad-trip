import re
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from src.domain.base_schema import BaseSchema
from src.domain.enums import Status


class CreateDriverSchema(BaseSchema):
    phone_number: str
    license_number: str
    license_issued_at: date
    license_expires_at: date

    @field_validator("phone_number")
    def validate_phone(cls, v):
        cleaned = re.sub(r"[^\d+]", "", v)

        if not re.fullmatch(r"\+7\d{10}", cleaned):
            raise ValueError("Phone number must be in format +7XXXXXXXXXX")

        return cleaned

class DriverSchema(BaseModel):
    id: int
    user_id: int
    id_photo_url: str
    phone_number: str
    license_number: str
    license_photo_url: str
    license_issued_at: date
    license_expires_at: date
    status: Status
    rejection_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class UpdateDriverSchema(BaseSchema):
    phone_number: Optional[str] = None
    license_number: Optional[str] = None
    licence_issued_at: Optional[date] = None
    license_expires_at: Optional[date] = None

    @field_validator("phone_number")
    def validate_phone(cls, v):
        if v is None:
            return v

        cleaned = re.sub(r"[^\d+]", "", v)

        if not re.fullmatch(r"\+7\d{10}", cleaned):
            raise ValueError("Phone number must be in format +7XXXXXXXXXX")

        return cleaned

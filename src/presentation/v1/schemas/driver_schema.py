from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel

from src.domain.base_schema import BaseSchema
from src.domain.enums import Status


class CreateDriverSchema(BaseSchema):
    phone_number: str
    license_number: str
    license_issued_at: date
    license_expires_at: date

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

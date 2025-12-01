from datetime import date
from typing import Optional

from src.domain.base_schema import BaseSchema


class CreateDriverSchema(BaseSchema):
    phone_number: str
    license_number: str
    license_issued_at: date
    license_expires_at: date

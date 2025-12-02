from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from src.domain.base_schema import BaseSchema, PaginationSchema
from src.domain.enums import Status


class CreateCompanySchema(BaseSchema):
    name: str
    bin: str
    description: str
    address: str

class CompanySchema(BaseModel):
    id: int
    name: str
    bin: str
    description: str
    address: str
    logo_url: str
    status: Status
    rejection_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        use_enum_values = True

class PaginationCompanySchema(PaginationSchema):
    items: Optional[List[CompanySchema]] = None

class UpdateCompanySchema(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
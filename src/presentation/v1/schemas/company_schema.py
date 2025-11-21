from typing import Optional

from pydantic import BaseModel

from src.domain.base_schema import BaseSchema
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

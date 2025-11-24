from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from fastapi import UploadFile

from src.domain.base_dto import BaseDTOMixin, PaginationDTO
from src.domain.enums import Status


@dataclass
class CompanyDTO(BaseDTOMixin):
    id: Optional[int] = None
    owner_id: Optional[int] = None
    name: Optional[str] = None
    bin: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    logo_url: Optional[str] = None
    status: Optional[Status] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    logo_file: Optional[UploadFile] = None

@dataclass
class PaginationCompanyDTO(BaseDTOMixin, PaginationDTO):
    items: Optional[List[CompanyDTO]] = None
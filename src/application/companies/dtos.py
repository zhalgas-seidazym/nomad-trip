from dataclasses import dataclass
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
    logo_file: Optional[UploadFile] = None
    rejection_reason: Optional[str] = None

@dataclass
class PaginationCompanyDTO(BaseDTOMixin, PaginationDTO):
    items: Optional[List[CompanyDTO]] = None
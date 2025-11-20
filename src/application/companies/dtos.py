from dataclasses import dataclass
from typing import Optional

from fastapi import UploadFile

from src.domain.base_dto import BaseDTOMixin
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
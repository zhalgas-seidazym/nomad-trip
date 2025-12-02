from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, List

from fastapi import UploadFile

from src.domain.base_dto import BaseDTOMixin, PaginationDTO
from src.domain.enums import Status


@dataclass
class DriverCompanyDTO(BaseDTOMixin):
    driver_id: Optional[int] = None
    company_id: Optional[int] = None
    status: Optional[Status] = None
    rejection_reason: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class DriverDTO(BaseDTOMixin):
    id: Optional[int] = None
    user_id: Optional[int] = None
    id_photo_url: Optional[str] = None
    phone_number: Optional[str] = None
    license_number: Optional[str] = None
    license_photo_url: Optional[str] = None
    license_issued_at: Optional[date] = None
    license_expires_at: Optional[date] = None
    status: Optional[Status] = None
    rejection_reason: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    id_photo_file: Optional[UploadFile] = None
    license_photo_file: Optional[UploadFile] = None

@dataclass
class PaginationDriverDTO(BaseDTOMixin, PaginationDTO):
    items: Optional[List[DriverDTO]] = None

@dataclass
class PaginationDriverCompanyDTO(BaseDTOMixin, PaginationDTO):
    items: Optional[List[DriverCompanyDTO]] = None

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.domain.base_dto import BaseDTOMixin
from src.domain.enums import UserRoles


@dataclass
class UserDTO(BaseDTOMixin):
    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRoles] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
from dataclasses import dataclass
from typing import Optional

from src.domain.base_dto import BaseDTOMixin


@dataclass
class UserDTO(BaseDTOMixin):
    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    password2: Optional[str] = None
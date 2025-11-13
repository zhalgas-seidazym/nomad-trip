from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from fastapi import Response

from src.application.users.dtos import UserDTO


class IUserController(ABC):
    @abstractmethod
    async def send_otp(self, user: UserDTO): ...

    @abstractmethod
    async def validate_otp(self, user: UserDTO, code: str, response: Response): ...

    @abstractmethod
    async def get_profile(self, user_id: int): ...

    @abstractmethod
    async def update(self, user_id: int, user_data: UserDTO): ...

    @abstractmethod
    async def delete(self, user_id: int): ...

    @abstractmethod
    async def refresh_token(self, refresh_token: str, response: Response): ...

class IUserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[UserDTO]: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserDTO]: ...

    @abstractmethod
    async def add(self, user_data: Dict[str, Any]) -> Optional[UserDTO]: ...

    @abstractmethod
    async def update(self, user_id: int, user_data: Dict[str, Any]) -> Optional[UserDTO]: ...

    @abstractmethod
    async def delete(self, user_id: int) -> None: ...

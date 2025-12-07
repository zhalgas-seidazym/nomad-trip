from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Protocol

from fastapi import Response

from src.application.users.dtos import UserDTO


class IUserController(ABC):
    @abstractmethod
    async def send_otp(self, email: str) -> Dict: ...

    @abstractmethod
    async def verify_otp(self, user_data: UserDTO, code: str, response: Response) -> Dict: ...

    @abstractmethod
    async def login(self, user_data: UserDTO, response: Response) -> Dict: ...

    @abstractmethod
    async def get_profile(self, user_id: int) -> Dict: ...

    @abstractmethod
    async def update(self, user: UserDTO, user_data: UserDTO) -> Dict: ...

    @abstractmethod
    async def change_password(self, user_data: UserDTO, code: str) -> Dict: ...

    @abstractmethod
    async def delete(self, user_id: int) -> Dict: ...

    @abstractmethod
    async def refresh_token(self, refresh_token: str, response: Response) -> Dict: ...

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
    async def delete(self, user_id: int) -> Optional[bool]: ...

class IEmailOtpService(Protocol):
    async def send_otp(self, email: str) -> None: ...

    async def verify_otp(self, email: str, code: str) -> None: ...
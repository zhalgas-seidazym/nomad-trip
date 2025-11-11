from typing import Protocol, Optional

class IJWTService(Protocol):
    def create_token(
        self,
        data: dict,
        expires_delta: Optional[int] = None,
        is_access_token: bool = True
    ) -> str:
        ...

    def verify_token(self, token: str) -> dict:
        ...


class IEmailService(Protocol):
    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        html: bool = False
    ) -> None:
        ...

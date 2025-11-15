from datetime import time
from typing import Optional

from dependency_injector.wiring import inject, Provide
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.app.container import container
from src.application.users.interfaces import IUserRepository
from src.domain.interfaces import IJWTService
from src.presentation.v1.depends.repositories import get_user_repository

http_bearer = HTTPBearer()

@inject
async def get_current_user(
        token: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer),
        jwt_service: IJWTService = Depends(Provide[container.jwt_service]),
        user_repo: IUserRepository = Depends(get_user_repository),
):
    if token is None or not token.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    if token.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    payload = jwt_service.decode_token(token.credentials)
    exp = payload['exp']

    if time.time() >= int(exp):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    user = await user_repo.get_by_id(payload['user_id'])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    return user
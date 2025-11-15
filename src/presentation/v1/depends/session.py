from typing import AsyncGenerator

from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.app.container import container

@inject
async def get_session(
        session_factory: async_sessionmaker[AsyncSession] = Depends(
            Provide[container.session_factory]
        ),
) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session
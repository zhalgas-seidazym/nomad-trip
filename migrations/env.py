import sys
import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine

sys.path.append("src")

from src.infrastructure.dbs.postgre import Base
from src.app.config.config import Settings
from src.application.users.models import User

settings = Settings()

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

db_url = settings.db_url

target_metadata = Base.metadata


# -----------------------
# OFFLINE режим (без async)
# -----------------------
def run_migrations_offline() -> None:
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# -----------------------
# ONLINE режим (async)
# -----------------------
async def run_migrations_online() -> None:
    connectable: AsyncEngine = create_async_engine(db_url, pool_pre_ping=True)

    async with connectable.connect() as connection:
        await connection.run_sync(
            lambda sync_connection: context.configure(
                connection=sync_connection,
                target_metadata=target_metadata,
                compare_type=True,
            )
        )

        await connection.run_sync(
            lambda sync_connection: context.begin_transaction()
        )
        await connection.run_sync(
            lambda sync_connection: context.run_migrations()
        )


def run_async_migrations():
    asyncio.run(run_migrations_online())


# -----------------------
# Запуск
# -----------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_async_migrations()

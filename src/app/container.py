from dependency_injector import containers, providers

from src.app.config.config import Settings
from src.infrastructure.dbs.postgre import create_engine, create_session_factory
from src.infrastructure.dbs.redis import RedisConnection


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.presentation.v1.depends.session",
            "src.presentation.v1.depends.security",
            "src.presentation.v1.depends.controllers",
        ]
    )

    settings = Settings()

    engine = providers.Singleton(create_engine, db_url=settings.db_url, echo=False)

    session_factory = providers.Resource(
        create_session_factory, engine=engine
    )

    redis = providers.Resource(RedisConnection, db_url=settings.REDIS_URL)


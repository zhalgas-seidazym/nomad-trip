from dependency_injector import containers, providers

from src.app.config.config import Settings
from src.infrastructure.dbs.postgre import create_engine, create_session_factory


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.presentation.depends.session",
            "src.presentation.depends.security",
            "src.presentation.depends.controllers",
        ]
    )

    settings = Settings()

    engine = providers.Singleton(create_engine, db_url=settings.db_url, echo=False)

    session_factory = providers.Resource(
        create_session_factory, engine=engine
    )


from dependency_injector import containers, providers

from src.app.config.config import Settings
from src.application.users.services import EmailOtpService
from src.infrastructure.dbs.postgre import create_engine, create_session_factory
from src.infrastructure.dbs.redis import RedisConnection
from src.infrastructure.integrations.jwt_service import JWTService
from src.infrastructure.integrations.email_service import AsyncEmailService


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

    email_service = providers.Factory(
        AsyncEmailService,
        smtp_host=settings.SMTP_HOST,
        smtp_port=settings.SMTP_PORT,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASSWORD,
        from_email=settings.SMTP_FROM,
    )

    jwt_service = providers.Factory(
        JWTService,
        jwt_secret=settings.JWT_SECRET,
        jwt_algorithm=settings.JWT_ALGORITHM,
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    email_otp_service = providers.Factory(
        EmailOtpService,
        email_service=AsyncEmailService,
        redis=redis,
        otp_ttl=settings.OTP_TTL,
    )


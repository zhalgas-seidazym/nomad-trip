from sqlalchemy import String, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.base_model import TimestampMixin
from src.infrastructure.dbs.postgre import Base
from src.domain.enums import UserRoles


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRoles] = mapped_column(Enum(UserRoles), nullable=False, default=UserRoles.PASSENGER)
    avatar_url: Mapped[str] = mapped_column(String, nullable=True)

    company = relationship("Company", back_populates="owner", uselist=False, cascade="all, delete")
    driver = relationship("Driver", back_populates="user", uselist=False, cascade="all, delete")
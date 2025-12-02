from sqlalchemy import String, Integer, ForeignKey, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.application.drivers.models import driver_company_table
from src.infrastructure.dbs.postgre import Base
from src.domain.base_model import TimestampMixin
from src.domain.enums import Status


class Company(Base, TimestampMixin):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, unique=True, index=True
    )

    name: Mapped[str] = mapped_column(String, nullable=False)
    bin: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    logo_url: Mapped[str] = mapped_column(String, nullable=False)

    status: Mapped[Status] = mapped_column(
        Enum(Status),
        nullable=False,
        default=Status.WAITING
    )
    rejection_reason: Mapped[str] = mapped_column(
        Text,
        nullable=True,
        default=None
    )

    owner = relationship("User", back_populates="company")

    drivers = relationship(
        "Driver",
        secondary=driver_company_table,
        back_populates="companies",
        passive_deletes=True
    )

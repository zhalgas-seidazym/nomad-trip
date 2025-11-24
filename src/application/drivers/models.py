from datetime import date

from sqlalchemy import String, Integer, ForeignKey, Enum, Text, Table, Column, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.infrastructure.dbs.postgre import Base
from src.domain.base_model import TimestampMixin
from src.domain.enums import Status


driver_company_table = Table(
    "driver_company",
    Base.metadata,
    Column("driver_id", Integer, ForeignKey("drivers.id", ondelete="CASCADE"), primary_key=True),
    Column("company_id", Integer, ForeignKey("companies.id", ondelete="CASCADE"), primary_key=True),
    Column("status", Enum(Status), default=Status.WAITING, nullable=False)
)

class Driver(Base, TimestampMixin):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)

    id_photo_url: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)

    license_number: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    license_photo_url: Mapped[str] = mapped_column(String, nullable=False)

    license_issued_at: Mapped[date] = mapped_column(Date, nullable=False)
    license_expires_at: Mapped[date] = mapped_column(Date, nullable=False)

    status: Mapped[Status] = mapped_column(Enum(Status), nullable=False, default=Status.WAITING)
    rejection_reason: Mapped[str] = mapped_column(Text, nullable=True, default=None)

    user = relationship("User", back_populates="driver")

    companies = relationship(
        "Company",
        secondary="driver_company",
        back_populates="drivers"
    )
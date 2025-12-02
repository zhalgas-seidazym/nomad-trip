from datetime import date

from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from sqlalchemy import String, Integer, ForeignKey, Enum, Text, Table, Column, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.infrastructure.dbs.postgre import Base
from src.domain.base_model import TimestampMixin
from src.domain.enums import Status


status_enum = PGEnum(
    'APPROVED', 'REJECTED', 'WAITING',
    name='status',
    create_type=False
)

driver_company_table = Table(
    "driver_company",
    Base.metadata,
    Column("driver_id", Integer, ForeignKey("drivers.id", ondelete="CASCADE"), primary_key=True),
    Column("company_id", Integer, ForeignKey("companies.id", ondelete="CASCADE"), primary_key=True),
    Column("status", status_enum, nullable=False, default=Status.WAITING),
    Column("rejection_reason", Text, nullable=True, default=None),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
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

    status: Mapped[Status] = mapped_column(
        status_enum,
        nullable=False,
        default=Status.WAITING
    )

    rejection_reason: Mapped[str] = mapped_column(Text, nullable=True, default=None)

    user = relationship("User", back_populates="driver")

    companies = relationship(
        "Company",
        secondary="driver_company",
        back_populates="drivers"
    )
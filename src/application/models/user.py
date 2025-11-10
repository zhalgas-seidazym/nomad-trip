from sqlalchemy import Column, Integer, String, Enum

from src.domain.base_model import TimestampMixin
from src.infrastructure.dbs.postgre import Base
from src.domain.enums import UserRoles

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRoles), nullable=False, default=UserRoles.PASSENGER)

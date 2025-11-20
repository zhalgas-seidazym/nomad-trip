from enum import Enum

class UserRoles(str, Enum):
    ADMIN = "admin"
    PASSENGER = "passenger"
    DRIVER = "driver"
    COMPANY = "company"

class Status(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    WAITING = "waiting"
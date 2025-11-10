from enum import Enum

class UserRoles(str, Enum):
    ADMIN = "admin"
    PASSENGER = "passenger"
    DRIVER = "driver"

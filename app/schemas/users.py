import uuid
from enum import Enum

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    """Schema for reading user data"""

    pass


class UserCreate(schemas.BaseUserCreate):
    """Schema for creating users"""

    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Schema for updating users"""

    pass


class GenderEnum(str, Enum):
    """Enumeration for gender options"""

    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

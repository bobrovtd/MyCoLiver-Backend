import uuid
from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel

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


class UserProfileBase(BaseModel):
    """Base schema for user profile data"""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[GenderEnum] = None
    looking_for: Optional[GenderEnum] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    age_min: int = 18
    age_max: int = 99
    distance_max: int = 50
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class UserProfileCreate(UserProfileBase):
    """Schema for creating a user profile"""

    pass


class UserProfileUpdate(UserProfileBase):
    """Schema for updating a user profile"""

    pass


class UserProfileRead(UserProfileBase):
    """Schema for reading a user profile"""

    id: uuid.UUID
    user_id: uuid.UUID

    model_config = {"from_attributes": True}


class UserImageBase(BaseModel):
    """Base schema for user images"""

    image_url: str
    is_primary: bool = False


class UserImageCreate(UserImageBase):
    """Schema for creating a user image"""

    pass


class UserImageUpdate(UserImageBase):
    """Schema for updating a user image"""

    pass


class UserImageRead(UserImageBase):
    """Schema for reading a user image"""

    id: uuid.UUID
    user_id: uuid.UUID

    model_config = {"from_attributes": True}

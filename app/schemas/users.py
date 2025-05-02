import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    """Schema for reading user data"""

    # Add custom fields here
    pass


class UserCreate(schemas.BaseUserCreate):
    """Schema for creating users"""

    # Add custom fields here
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Schema for updating users"""

    # Add custom fields here
    pass

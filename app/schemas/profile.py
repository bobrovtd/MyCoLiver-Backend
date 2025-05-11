from pydantic import BaseModel, Field
from typing import Optional
import uuid
from datetime import date
from app.schemas.users import GenderEnum


class UserProfileCreate(BaseModel):
    user_id: uuid.UUID
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    bio: Optional[str] = Field(None, max_length=500)
    gender: Optional[GenderEnum]
    birth_date: Optional[date]
    image_url: Optional[str]
    is_primary_image: Optional[bool] = False


class UserProfileUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    bio: Optional[str] = Field(None, max_length=500)
    gender: Optional[GenderEnum]
    birth_date: Optional[date]
    image_url: Optional[str]
    is_primary_image: Optional[bool]


class UserProfileResponse(UserProfileCreate):
    id: uuid.UUID

    class Config:
        orm_mode = True

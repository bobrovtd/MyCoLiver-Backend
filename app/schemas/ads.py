from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from decimal import Decimal
from app.models.ads import Gender


class AdCreate(BaseModel):
    owner_id: UUID
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    age_requirements: Optional[int] = None
    nationality: Optional[str] = None
    budget: Optional[Decimal] = None
    number_of_roommates: Optional[int] = None
    gender: Optional[Gender] = None
    bad_habits: Optional[str] = None
    cleanliness: Optional[str] = None
    character: Optional[str] = None
    lifestyle: Optional[str] = None


class AdUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    age_requirements: Optional[int] = None
    nationality: Optional[str] = None
    budget: Optional[Decimal] = None
    number_of_roommates: Optional[int] = None
    gender: Optional[Gender] = None
    bad_habits: Optional[str] = None
    cleanliness: Optional[str] = None
    character: Optional[str] = None
    lifestyle: Optional[str] = None


class AdResponse(AdCreate):
    ad_id: UUID

    class Config:
        orm_mode = True

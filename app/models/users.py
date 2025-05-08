import uuid
import enum
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey, Date, Integer, Float, Enum
from sqlalchemy.dialects.postgresql import UUID

from app.database.base import Base


class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"


class User(SQLAlchemyBaseUserTableUUID, Base):
    """
    User model that extends the base FastAPI Users model.
    Contains only authentication-related data.
    """

    __tablename__ = "users"

    # FastAPI Users already provides: id, email, hashed_password, is_active, is_verified, is_superuser

    # Relationship with profile
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    # Relationship with images
    images = relationship("UserImage", back_populates="user")


class UserProfile(Base):
    """
    Model for storing user profile data separate from authentication data.
    Contains personal information and preferences.
    """

    __tablename__ = "user_profiles"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False
    )

    # Personal information
    first_name = mapped_column(String(50))
    last_name = mapped_column(String(50))
    birth_date = mapped_column(Date)
    gender = mapped_column(Enum(Gender))
    looking_for = mapped_column(Enum(Gender))
    bio = mapped_column(String(500))
    location = mapped_column(String(100))

    # Search preferences
    age_min = mapped_column(Integer, default=18)
    age_max = mapped_column(Integer, default=99)
    distance_max = mapped_column(Integer, default=50)  # in kilometers

    # Geolocation data
    latitude = mapped_column(Float)
    longitude = mapped_column(Float)

    # Relationship with user
    user = relationship("User", back_populates="profile")


class UserImage(Base):
    """
    Model for storing user profile images.
    """

    __tablename__ = "user_images"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    image_url = mapped_column(String, nullable=False)
    is_primary = mapped_column(Boolean, default=False)

    # Relationship with user
    user = relationship("User", back_populates="images")

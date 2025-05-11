import uuid
import enum

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey, Date, Integer, Float, Enum
from sqlalchemy.dialects.postgresql import UUID

from app.database.base import Base


class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"


class UserProfile(Base):
    """
    Model for storing user profile data, including personal information,
    preferences, and associated image data.
    """

    __tablename__ = "profiles"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False
    )

    # Personal information
    first_name = mapped_column(String(50))
    last_name = mapped_column(String(50))
    bio = mapped_column(String(500))
    gender = mapped_column(Enum(Gender))
    birth_date = mapped_column(Date)

    # Image information
    image_url = mapped_column(String, nullable=True)

    # Relationship with user
    user = relationship("User", back_populates="profile")

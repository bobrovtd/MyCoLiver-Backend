import enum
import uuid

from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer, Numeric, Text, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.database.base import Base


class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class Ad(Base):
    """
    Model for storing advertisement data, including personal preferences and roommate requirements.
    """

    __tablename__ = "ads"

    ad_id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Ad details
    title = mapped_column(String(255), nullable=False)
    description = mapped_column(Text, nullable=True)

    # Requirements and preferences
    age_requirements = mapped_column(Integer, nullable=True)
    nationality = mapped_column(String(100), nullable=True)
    budget = mapped_column(Numeric, nullable=True)
    number_of_roommates = mapped_column(Integer, nullable=True)
    gender = mapped_column(Enum(Gender), nullable=True)
    bad_habits = mapped_column(String(255), nullable=True)
    cleanliness = mapped_column(String(255), nullable=True)
    character = mapped_column(String(255), nullable=True)
    lifestyle = mapped_column(String(255), nullable=True)

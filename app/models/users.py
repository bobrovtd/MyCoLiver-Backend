from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import relationship

from app.database.base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    """
    User model that extends the base FastAPI Users model.
    Contains only authentication-related data.
    """

    __tablename__ = "users"

    # FastAPI Users already provides: id, email, hashed_password, is_active, is_verified, is_superuser

    # Relationship with profile
    profile = relationship("UserProfile", back_populates="user", uselist=False)

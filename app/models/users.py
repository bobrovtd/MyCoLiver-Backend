import uuid
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import mapped_column
from sqlalchemy import String

from app.database.base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    """
    User model that extends the base FastAPI Users model.
    Add custom fields here as needed.
    """

    # Example of a custom field
    # full_name = mapped_column(String(255), nullable=True)
    pass

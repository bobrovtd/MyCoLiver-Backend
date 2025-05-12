# Import models here for Alembic to detect them
from app.models.users import User
from app.models.profiles import UserProfile
from app.models.ads import Ad

__all__ = ["User", "UserProfile", "Ad"]

# This file makes the directory a Python package
from app.routers import profiles, ads, auth, users

# The auth and users routers are handled directly by FastAPI Users
# in the main.py file, so we don't need to include them here
__all__ = ["profiles", "auth", "users", "ads"]
from fastapi import APIRouter

from app.routers import auth, users

api_router = APIRouter()

# Include routers from modules
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])

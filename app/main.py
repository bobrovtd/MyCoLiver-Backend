from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.auth.users import auth_backend, fastapi_users
from app.core.config import settings
from app.core.logger import configure_logging, get_logger
from app.database.config import create_db_and_tables
from app.routers import profiles, ads
from app.schemas.users import UserCreate, UserRead, UserUpdate

# Configure logging
configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager to handle setup and cleanup tasks at application lifecycle boundaries.
    """
    if settings.DEBUG:
        logger.info("Application startup: Running in DEBUG mode. Creating database tables...")
        await create_db_and_tables()
        logger.info("Database tables created successfully")
    yield  # Application runs here
    # Cleanup actions, if necessary, can be added here (e.g., closing connections)


def create_application() -> FastAPI:
    """
    Factory function to create the FastAPI application
    """
    application = FastAPI(
        lifespan=lifespan,
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Set up CORS middleware
    if settings.BACKEND_CORS_ORIGINS:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Register FastAPI Users routes
    application.include_router(
        fastapi_users.get_auth_router(auth_backend),
        prefix=f"{settings.API_V1_STR}/auth/jwt",
        tags=["auth"],
    )
    application.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix=f"{settings.API_V1_STR}/auth",
        tags=["auth"],
    )
    application.include_router(
        fastapi_users.get_reset_password_router(),
        prefix=f"{settings.API_V1_STR}/auth",
        tags=["auth"],
    )
    application.include_router(
        fastapi_users.get_verify_router(UserRead),
        prefix=f"{settings.API_V1_STR}/auth",
        tags=["auth"],
    )
    application.include_router(
        fastapi_users.get_users_router(UserRead, UserUpdate),
        prefix=f"{settings.API_V1_STR}/users",
        tags=["users"],
    )

    # Register other routes
    application.include_router(
        profiles.router,
        prefix=f"{settings.API_V1_STR}/profiles",
        tags=["profiles"],
    )
    application.include_router(
        ads.router,
        prefix=f"{settings.API_V1_STR}/ads",
        tags=["ads"],
    )

    # Root endpoint
    @application.get("/", tags=["Status"])
    async def root():
        return {
            "status": "online",
            "message": f"Welcome to the {settings.PROJECT_NAME}. Visit /docs for API documentation.",
        }

    return application


app = create_application()


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        # host=settings.HOST,
        # port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower(),
        reload=settings.DEBUG
    )
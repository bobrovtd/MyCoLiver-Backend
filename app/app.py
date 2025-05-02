from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logger import configure_logging, get_logger
from app.database.config import create_db_and_tables
from app.routers import api_router

# Configure logging
configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup if not using migrations
    if settings.DEBUG:
        logger.info("Running in DEBUG mode. Creating database tables...")
        await create_db_and_tables()
        logger.info("Database tables created successfully")
    yield


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

    # Set CORS middleware
    if settings.BACKEND_CORS_ORIGINS:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Include API router
    application.include_router(api_router, prefix=settings.API_V1_STR)

    # Root endpoint
    @application.get("/", tags=["Status"])
    async def root():
        return {
            "status": "online",
            "message": f"Welcome to the {settings.PROJECT_NAME}. Visit /docs for API documentation.",
        }

    return application


app = create_application()

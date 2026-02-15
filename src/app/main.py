from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .db import init_db
from .routers import auth as auth_router, tasks as tasks_router
from .config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting up application...")
    # Only initialize DB via SQLAlchemy `create_all()` when explicitly enabled.
    # Prefer Alembic migrations for schema management in Docker-based workflows.
    try:
        from .config import settings

        if getattr(settings, "INIT_DB", False):
            await init_db()
            logger.info("Database initialized")
        else:
            logger.info("Skipping SQLAlchemy create_all(); use Alembic migrations instead")
    except Exception:
        logger.exception("Error during optional database init")
    yield
    logger.info("Shutting down application...")


app = FastAPI(
    title="task-manager-backend",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(tasks_router.router)


@app.get("/")
async def root():
    return {"message": "task-manager-backend is running"}


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }

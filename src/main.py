from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.database import reset_sqlite_database
from src.routes.movies import router as movie_router
from src.database.session import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await reset_sqlite_database()
    yield
    await close_db()


app = FastAPI(
    title="Movies homework",
    description="Description of project",
    lifespan=lifespan
)

api_version_prefix = "/api/v1"

app.include_router(movie_router, prefix=f"{api_version_prefix}/theater", tags=["theater"])

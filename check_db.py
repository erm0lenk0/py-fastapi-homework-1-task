import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func
from src.database.models import MovieModel

async def check_movies():
    engine = create_async_engine("sqlite+aiosqlite:///./src/database/source/movies.db")
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        result = await session.execute(select(func.count()).select_from(MovieModel))
        print("Количество фильмов в базе:", result.scalar())

if __name__ == "__main__":
    asyncio.run(check_movies())

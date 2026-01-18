from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from math import ceil

from src.database.session import get_db
from src.database.models import MovieModel
from src.schemas.movies import (
    MovieDetailResponseSchema,
    MovieListResponseSchema,
)

router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("", response_model=MovieListResponseSchema)
@router.get("/", response_model=MovieListResponseSchema)
async def list_movies(
    page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        db: AsyncSession = Depends(get_db),
):

    result = await db.execute(select(MovieModel))
    all_movies = result.scalars().all()
    total_items = len(all_movies)

    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = ceil(total_items / per_page)

    if page > total_items:
        raise HTTPException(status_code=404, detail="No movies found.")

    start = (page - 1) * per_page
    end = start + per_page
    movies_slice = all_movies[start:end]

    if not movies_slice:
        raise HTTPException(status_code=404, detail="No movies found.")

    movie_items = [
        MovieDetailResponseSchema(
            id=m.id,
            name=m.name,
            date=str(m.date),
            score=float(m.score),
            genre=m.genre,
            overview=m.overview,
            crew=m.crew,
            orig_title=m.orig_title,
            status=m.status,
            orig_lang=m.orig_lang,
            budget=float(m.budget) if m.budget is not None else 0.0,
            revenue=m.revenue,
            country=m.country,
        )
        for m in movies_slice
    ]

    prev_page = None if page == 1 else f"/api/v1/theater/movies/?page={page-1}&per_page={per_page}"
    next_page = None if page == total_pages else f"/api/v1/theater/movies/?page={page+1}&per_page={per_page}"

    return MovieListResponseSchema(
        movies=movie_items,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )

@router.get("/{movie_id}/", response_model=MovieDetailResponseSchema)
@router.get("/{movie_id}", response_model=MovieDetailResponseSchema)
async def get_movie_detail(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
):

    movie = await db.get(MovieModel, movie_id)

    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")

    return MovieDetailResponseSchema(
        id=movie.id,
        name=movie.name,
        date=str(movie.date),
        score=float(movie.score),
        genre=movie.genre,
        overview=movie.overview,
        crew=movie.crew,
        orig_title=movie.orig_title,
        status=movie.status,
        orig_lang=movie.orig_lang,
        budget=int(movie.budget) if movie.budget is not None else 0.0,
        revenue=movie.revenue,
        country=movie.country,
    )
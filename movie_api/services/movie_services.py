from typing import Any, Dict, List

from flask_sqlalchemy import BaseQuery

from movie_api.core.exceptions import QuokkaException
from movie_api.entity.movie import MovieEntity
from movie_api.repository import movie_repository


def get_all_movies() -> BaseQuery:
    try:
        return movie_repository.get_all_movies()
    except Exception as e:
        raise e


def _validate_year(year: int) -> int:
    if isinstance(year, int):
        return year
    try:
        return int(year)
    except Exception:
        raise QuokkaException(code=400, description="Invalid year value")


def get_movies_by_year(year: int) -> BaseQuery:
    try:
        valid_year = _validate_year(year=year)
        return movie_repository.get_movies_by_year(year=valid_year)
    except Exception as e:
        raise e


def get_movies_by_tags(tags: List[str]) -> BaseQuery:
    try:
        return movie_repository.get_movies_by_tags(tags=tags)
    except Exception as e:
        raise e


def create_movie(payload: Dict[str, Any]) -> BaseQuery:
    try:
        return movie_repository.create_movie(payload=MovieEntity.from_dict(payload))
    except Exception as e:
        raise e

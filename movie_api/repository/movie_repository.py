from typing import List, Optional

from flask_sqlalchemy import BaseQuery

from movie_api.db.models.movie import Movie, Tag
from movie_api.entity.movie import MovieEntity


def get_all_movies() -> BaseQuery:
    return Movie.query.filter(True)


def get_movies_by_year(year: int) -> BaseQuery:
    return get_all_movies().filter(Movie.year == year)


def get_movies_by_tags(tags: Optional[List[str]]) -> BaseQuery:
    all_movies_q: BaseQuery = get_all_movies()
    if tags is None:
        return all_movies_q
    return all_movies_q.filter(Movie.tags.any(Tag.name.in_(tags)))


def get_or_create_tag(tag: str) -> Tag:
    tag_q: BaseQuery = Tag.query.filter(Tag.name == tag)
    if tag_q.count() > 0:
        return tag_q.first()
    return Tag.create(name=tag)


def create_movie(payload: MovieEntity) -> Movie:
    payload_dict = payload.asdict()
    tags_str: List[str] = payload_dict.pop("tags")
    m: Movie = Movie.create(**payload_dict)
    for t in tags_str:
        t_instance: Tag = get_or_create_tag(tag=t)
        m.tags.append(t_instance)
    m.commit()
    return m

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship

from movie_api.db.models.base import BaseIntPrimaryModel, BaseUuidPrimaryModel


class Genre(BaseUuidPrimaryModel):
    __tablename__ = "genre"
    name = Column(String())

    movies = relationship("Movie", lazy="dynamic")


class Tag(BaseUuidPrimaryModel):
    __tablename__ = "tag"
    name = Column(String())

    movies = relationship("Movie", secondary="movie_tag", lazy="dynamic")


class Movie(BaseUuidPrimaryModel):
    __tablename__ = "movie"
    title = Column(String(100))
    description = Column(String(), nullable=True)
    genre_id = Column(
        UUID(as_uuid=True), ForeignKey("genre.id", ondelete="SET NULL"), nullable=True
    )
    year = Column(Integer())
    image_url = Column(String(), nullable=True)

    genre = relationship("Genre", uselist=False)
    tags = relationship("Tag", secondary="movie_tag", lazy="dynamic")


class MovieTag(BaseIntPrimaryModel):
    __tablename__ = "movie_tag"
    movie_id = Column(UUID(as_uuid=True), ForeignKey("movie.id", ondelete="CASCADE"))
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tag.id", ondelete="CASCADE"))

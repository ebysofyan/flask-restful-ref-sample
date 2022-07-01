from factory.alchemy import SQLAlchemyModelFactory

from movie_api.db.models.base import scoped_session
from movie_api.db.models.movie import Movie


class MovieFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Movie
        sqlalchemy_session = scoped_session

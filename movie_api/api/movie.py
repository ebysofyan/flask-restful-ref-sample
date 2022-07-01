from typing import Any, Dict, Optional, Tuple, Union

from flask import request
from flask.blueprints import Blueprint
from flask_restful import Api
from flask_sqlalchemy import BaseQuery

from movie_api.api.base_api import BaseApi
from movie_api.core.exceptions import QuokkaException, make_exception
from movie_api.db.schemas.movie_schema import MovieSchema
from movie_api.db.schemas.validator.movie_schema_validator import (
    MovieSchemaValidator,
)
from movie_api.services import movie_services

movie_bp = Blueprint("movie", __name__)
rest_movie_bp = Api(movie_bp)


class MovieApiRoute(BaseApi):
    def get(self, **kwargs) -> Union[Optional[Dict[str, Any]], Tuple]:
        try:
            movies: BaseQuery = movie_services.get_all_movies()
            return self.make_response(
                message="Success",
                data=MovieSchema().dump(movies, many=True),
            )
        except Exception as e:
            return make_exception(e)

    def post(self) -> Union[Optional[Dict[str, Any]], Tuple]:
        try:
            data: Dict[str, Any] = request.get_json(force=True)
            errors = MovieSchemaValidator().validate(data)
            if bool(errors):
                raise QuokkaException(
                    400, description="Bad Request", errors_data=errors
                )
            movie = movie_services.create_movie(data)
            return self.make_response(
                message="Success",
                data=MovieSchema().dump(movie),
            )
        except Exception as e:
            return make_exception(e)


rest_movie_bp.add_resource(MovieApiRoute, "movies")

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from movie_api.db.models.movie import Genre, Movie, Tag


class TagSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tag
        include_fk = False
        load_instance = True
        exclude = ("time_created", "time_updated")


class GenreSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Genre
        include_fk = False
        load_instance = True
        exclude = ("time_created", "time_updated")


class MovieSchema(SQLAlchemyAutoSchema):
    genre = fields.Nested(GenreSchema)
    tags = fields.Nested(TagSchema, many=True)

    class Meta:
        model = Movie
        include_fk = False
        load_instance = True
        exclude = ("time_created", "time_updated")

from flask.app import Flask

from movie_api.api.movie import movie_bp


def register_api_blueprints(app: Flask) -> None:
    app.register_blueprint(movie_bp, url_prefix="/api/")

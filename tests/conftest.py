import pytest
from flask import Flask
from flask.testing import FlaskClient

from movie_api.config import get_config_path
from movie_api.context import movie_app as flask_app
from movie_api.db.models.base import DB
from movie_api.utils.db_helper import drop_everything

ADMIN_EMAIL = "admin@sample.com"
STAFF_EMAIL = "staff@sample.com"


@pytest.fixture
def app():
    flask_app.config.from_object("movie_api.config.TestingConfig")
    with flask_app.app_context():
        drop_everything(DB)
        DB.create_all()
        yield flask_app
        DB.session.remove()
        drop_everything(DB)
        flask_app.config.from_object(get_config_path())


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

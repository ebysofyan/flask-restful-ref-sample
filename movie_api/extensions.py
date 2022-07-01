from flask_apscheduler import APScheduler
from flask_celeryext import FlaskCeleryExt
from flask_cors import CORS
from flask_login import LoginManager
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from movie_api.celery_app import create_celery_app

db = SQLAlchemy(
    session_options={
        "autoflush": False,
        "autocommit": False,
    }
)
scheduler = APScheduler()
mail = Mail()
migrate = Migrate(compare_type=True)
cors = CORS()
marsh = Marshmallow()
login_manager = LoginManager()
celeryext = FlaskCeleryExt(create_celery_app=create_celery_app)

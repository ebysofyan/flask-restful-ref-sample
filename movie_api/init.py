from flask import Flask

from movie_api.blueprints import register_api_blueprints
from movie_api.config import ENABLE_SCHEDULER, TEMPLATES_DIR, get_config_path
from movie_api.extensions import (
    celeryext,
    cors,
    db,
    login_manager,
    mail,
    marsh,
    migrate,
    scheduler,
)
from movie_api.integrations.sentry import init_sentry


def create_app(name: str = __name__) -> Flask:
    app = Flask(name, template_folder=TEMPLATES_DIR)
    app.config.from_object(get_config_path())
    init_sentry()
    configure_extensions(app)
    register_api_blueprints(app)
    return app


def configure_extensions(app: Flask) -> None:
    db.init_app(app)
    app.DB = db
    migrate.init_app(app, db=db)
    cors.init_app(app)
    marsh.init_app(app)
    mail.init_app(app)
    app.mail = mail
    celeryext.init_app(app)
    login_manager.init_app(app)
    init_scheduler(app=app)


def init_scheduler(app: Flask) -> None:
    if ENABLE_SCHEDULER in ["True", "False"] and eval(ENABLE_SCHEDULER):
        app.scheduler = scheduler
        if not scheduler.running:
            scheduler.init_app(app)
            scheduler.start()

            @scheduler.authenticate
            def authenticate(auth):
                """Check auth."""
                username = scheduler.app.config["SCHEDULER_CREDENTIAL"]["username"]
                pasword = scheduler.app.config["SCHEDULER_CREDENTIAL"]["password"]
                return auth["username"] == username and auth["password"] == pasword

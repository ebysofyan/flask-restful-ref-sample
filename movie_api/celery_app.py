from celery import Celery
from celery import current_app as current_celery_app
from flask import Flask

app_modules = ("movie_api.tasks.sample",)


def create_celery_app(app: Flask) -> Celery:
    celery_app: Celery = current_celery_app
    celery_app.conf.update(app.config.get("CELERY", {}))

    class ContextTask(celery_app.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    celery_app.conf.imports = celery_app.conf.imports + app_modules
    return celery_app

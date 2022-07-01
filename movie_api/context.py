from celery import Celery

from movie_api.init import celeryext, create_app

movie_app = create_app()
context = movie_app.app_context()
celery_app: Celery = celeryext.celery


# @movie_app.after_request
# def handle_after_request(response):
# DB.session.expunge_all()
# DB.session.remove()
# Handle anything here
# return response

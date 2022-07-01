run-server:
	python -B app.py

run-celery_watch:
	watchmedo auto-restart -d . -R -p '*.py' -- celery -A movie_api.context.celery_app worker -E --loglevel=DEBUG

run-celery:
	celery -A movie_api.context.celery_app worker -E --loglevel=INFO

run-flower:
	celery -A movie_api.context.celery_app flower --address=0.0.0.0 --port=5566

run-test:
	python -m unittest discover -v

run-test_api:
	python movie_api/test_runner.py --pytest --verbose --tb=long ./tests/api/

run-migration:
	flask db stamp head
	flask db migrate
	flask db upgrade

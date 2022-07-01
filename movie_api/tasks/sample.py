import time

from movie_api.context import celery_app


@celery_app.task
def sample_task(arg: str) -> str:
    time.sleep(10)
    print(f"Print {arg} after 10 secs")
    return arg

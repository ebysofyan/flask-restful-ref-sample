import os

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from movie_api.config import SENTRY_DSN


def init_sentry() -> None:
    if os.getenv("ENV").lower() in ["staging", "prod", "production"]:
        try:
            sentry_sdk.init(
                dsn=SENTRY_DSN,
                integrations=[
                    FlaskIntegration(),
                    RedisIntegration(),
                    SqlalchemyIntegration(),
                ],
                traces_sample_rate=1.0,
            )
        finally:
            pass

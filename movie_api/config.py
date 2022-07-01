import json
import os

from dotenv import load_dotenv
from flask_apscheduler.auth import HTTPBasicAuth

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(basedir, ".env"))

__env = os.getenv("ENV")
BASE_DIR = basedir
TEMPLATES_DIR = os.path.join(basedir, "templates")
ENV = os.getenv("ENV")
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = os.getenv("MAIL_SERVER")
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")
QUOKKA_WEBSITE = os.getenv("QUOKKA_WEBSITE")
QUOKKA_ASSETS_PROFILE_PICTURE = os.getenv("QUOKKA_ASSETS_PROFILE_PICTURE")

S3_BUCKET = os.getenv("S3_BUCKET_NAME")
S3_LOCATION = f"https://{S3_BUCKET}.s3.amazonaws.com/"
S3_BUCKET_PROFILE_SUBDOMAIN = os.getenv("S3_BUCKET_PROFILE_SUBDOMAIN")
SENTRY_DSN = os.getenv("SENTRY_DSN")

DB_URL = os.getenv("DB_URL")
TEST_DB_URL = os.getenv("TEST_DB_URL")
HOST = os.getenv("HOST")
SECRET = os.getenv("SECRET")

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

CONFIG_TOTAL_WEEK_GOAL_REPORT = os.getenv("CONFIG_TOTAL_WEEK_GOAL_REPORT")
CONFIG_COUNT_WEEK_GOAL_REPORT = os.getenv("CONFIG_COUNT_WEEK_GOAL_REPORT")
CONFIG_COUNT_DAY_GOAL_REPORT_SCHEDULER = os.getenv(
    "CONFIG_COUNT_DAY_GOAL_REPORT_SCHEDULER"
)
ENABLE_SCHEDULER = os.getenv("ENABLE_SCHEDULER")
JOBS_LIST = json.loads(os.getenv("JOBS_LIST", "[]"))
SCHEDULER_API_ENABLED = os.getenv("SCHEDULER_API_ENABLED", True)
SCHEDULER_HOST = os.getenv("SCHEDULER_HOST", HOST)
SCHEDULER_CREDENTIAL = json.loads(os.getenv("SCHEDULER_CREDENTIAL", "{}"))

MANAGER_DASHBOARD_FEATURE_ENABLE = os.getenv("MANAGER_DASHBOARD_FEATURE_ENABLE", "1")
PROTOCOL_CONFIG = {
    "production": "https://",
    "prod": "https://",
    "staging": "https://",
    "development": "http://",
    "dev": "http://",
    "local": "http://",
    "test": "http://",
}
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_OAUTH_SCOPES = json.loads(os.getenv("SLACK_OAUTH_SCOPES", "[]"))
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

CELERY = {
    "broker_url": os.getenv("CELERY_BROKER_URL"),
    "result_backend": os.getenv("CELERY_RESULT_BACKEND_URL"),
}

ENABLE_API_ACCESS = os.getenv("ENABLE_API_ACCESS")
ENABLE_ADMIN_ACCESS = os.getenv("ENABLE_ADMIN_ACCESS")

PULSE_SURVEY_QUESTIONS_LIMIT = int(os.getenv("PULSE_SURVEY_QUESTIONS_LIMIT", 5))
PULSE_SURVEY_ROLLING_DAYS = int(os.getenv("PULSE_SURVEY_ROLLING_DAYS", 60))
PULSE_SURVEY_SKIPPED_QUESTION_VALUES = json.loads(
    os.getenv("PULSE_SURVEY_SKIPPED_QUESTION_VALUES", '["-1", "-2"]')
)
PULSE_SURVEY_ALLOW_MULTIPLE_RESPONSE_IN_SINGLE_PULSE = os.getenv(
    "PULSE_SURVEY_ALLOW_MULTIPLE_RESPONSE_IN_SINGLE_PULSE", "0"
)
PULSE_SURVEY_MOVING_AVERAGE_CALC_FUNCTION = os.getenv(
    "PULSE_SURVEY_MOVING_AVERAGE_CALC_FUNCTION",
    "movie_api.utils.engagement_report_calculation_helper.calculate_moving_average",
)
NPS_CATEGORIES_VALUE = {
    "promoters": (9, 10),
    "passives": (7, 8),
    "detractors": (0, 1, 2, 3, 4, 5, 6),
}
LIKERT_SCALE_NPS_CATEGORIES = {
    "positive": (4, 5),
    "neutral": (3,),
    "negative": (1, 2),
}
PULSE_SURVEY_RE_CALCULATION_TIME_SPAN = int(
    os.getenv("PULSE_SURVEY_RE_CALCULATION_TIME_SPAN", 120)
)


class BaseConfig:
    SECRET_KEY = SECRET
    ENV = os.getenv("ENV")
    FLASK_ENV = os.getenv("ENV")
    FLASK_APP = os.path.join(basedir, "movie_api", "app.py")

    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 1100,
        "pool_recycle": 120,
        "pool_pre_ping": True,
        "max_overflow": 1000,
    }
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    QUOKKA_WEBSITE = QUOKKA_WEBSITE
    MAIL_SERVER = MAIL_SERVER
    MAIL_PORT = MAIL_PORT
    MAIL_USE_SSL = MAIL_USE_SSL
    MAIL_USERNAME = MAIL_USERNAME
    MAIL_PASSWORD = MAIL_PASSWORD
    MAIL_DEFAULT_SENDER = MAIL_DEFAULT_SENDER
    MAIL_DEBUG = True
    SECRET = SECRET
    SECURITY_PASSWORD_SALT = SECURITY_PASSWORD_SALT
    JSON_SORT_KEYS = False

    SCHEDULER_API_ENABLED = True
    SCHEDULER_AUTH = HTTPBasicAuth()
    SCHEDULER_CREDENTIAL = SCHEDULER_CREDENTIAL
    SCHEDULER_EXECUTORS = {"default": {"type": "threadpool", "max_workers": 20}}
    SCHEDULER_JOB_DEFAULTS = {"coalesce": False, "max_instances": 7}

    TESTING = False
    JOBS = JOBS_LIST
    PROTOCOL = PROTOCOL_CONFIG[ENV]
    STRIPE_SECRET_KEY = STRIPE_SECRET_KEY
    SLACK_SIGNING_SECRET = SLACK_SIGNING_SECRET
    SLACK_BOT_TOKEN = SLACK_BOT_TOKEN
    GOOGLE_CLIENT_ID = GOOGLE_CLIENT_ID
    CELERY = CELERY
    SSE_REDIS_URL = os.getenv("SSE_REDIS_URL")
    REDIS_URL = os.getenv("SSE_REDIS_URL")


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = TEST_DB_URL
    TESTING = True
    # Uncomment this if using SQLite
    # SQLALCHEMY_ENGINE_OPTIONS = {}


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = DB_URL
    MAIL_DEBUG = True
    TESTING = False


class StagingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = DB_URL
    MAIL_DEBUG = True
    TESTING = False


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = DB_URL
    MAIL_DEBUG = False
    TESTING = False


def get_config_path() -> str:
    env = ENV.lower()
    if env == "staging":
        return "movie_api.config.StagingConfig"
    elif env in ["prod", "production"]:
        return "movie_api.config.ProductionConfig"
    return "movie_api.config.DevelopmentConfig"


def is_development_mode(include_staging: bool = False) -> bool:
    envs = ["local", "development", "test", "testing"]
    if include_staging:
        envs.append("staging")
    return os.getenv("ENV").lower() in envs

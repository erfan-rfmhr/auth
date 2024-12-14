import environ
from django.utils.crypto import get_random_string

from config.settings.components import BASE_DIR

env = environ.Env(
    DEBUG=(bool, True),
    # Security
    SECRET_KEY=(str, get_random_string(32)),
    SIGNING_KEY=(str, get_random_string(32)),
    # Database
    DB_NAME=(str, "auth_task_db"),
    DB_USER=(str, "postgres"),
    DB_PASSWORD=(str, "postgres"),
    DB_HOST=(str, "db"),
    DB_PORT=(int, 5432),
    # Redis
    REDIS_URL=(str, "redis://redis:6379/0"),
)
environ.Env.read_env(BASE_DIR / ".env")

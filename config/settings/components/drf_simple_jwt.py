from datetime import timedelta

from config.settings.components.env import env

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=365),
    "TOKEN_TYPE_CLAIM": "typ",
    "SIGNING_KEY": env("SIGNING_KEY"),
}

from config.settings.components.redis import REDIS_URL

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
            "SOCKET_TIMEOUT": 2,
            "SOCKET_CONNECT_TIMEOUT": 2,
        },
    },
}

OTP_TIMEOUT = 2 * 60
OTP_KEY_PREFIX = "otp_"
OTP_MAX_VALUE = 999_999
OTP_MIN_VALUE = 100_000

from config.settings.components.env import env

DJANGO_POSTGRES_ENGINE = "django.db.backends.postgresql"

DATABASES = {
    "default": {
        "ENGINE": DJANGO_POSTGRES_ENGINE,
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
        "DISABLE_SERVER_SIDE_CURSORS": True,
    },
}

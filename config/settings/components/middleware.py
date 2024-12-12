MIDDLEWARE_IN_START = [
    "corsheaders.middleware.CorsMiddleware",
]

MIDDLEWARE_DJANGO = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


MIDDLEWARE = (
    MIDDLEWARE_IN_START
    + MIDDLEWARE_DJANGO
)

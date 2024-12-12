INSTALLED_APPS_DJANGO = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS_LIBS = [
    "corsheaders",
    # DRF
    "rest_framework",
    "drf_spectacular",
]

INSTALLED_APPS_LOCAL = [
    "user",
]


INSTALLED_APPS = (
    INSTALLED_APPS_DJANGO
    + INSTALLED_APPS_LIBS
    + INSTALLED_APPS_LOCAL
)

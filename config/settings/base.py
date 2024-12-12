from .components.env import *  # noqa
from .components.database import *  # noqa
from .components.apps import *  # noqa
from .components.csrf import *  # noqa
from .components.url import *  # noqa
from .components.wsgi import *  # noqa
from .components.auth import *  # noqa
from .components.drf import *  # noqa
from .components.drf_simple_jwt import *  # noqa
from .components.drf_spectacular import *  # noqa
from .components.middleware import *  # noqa
from .components.cors_headers import *  # noqa
from .components.i18n import *  # noqa
from .components.session import *  # noqa
from .components.security import *  # noqa
from .components.redis import *  # noqa
from .components.fields import *  # noqa
from .components.cache import *  # noqa
from .components.templates import * # noqa
from .components.static_files import * # noqa
from .components.media import * # noqa

DEBUG = env('DEBUG')

if DEBUG:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }


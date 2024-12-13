from functools import wraps

from django.core.cache import cache
from rest_framework.exceptions import PermissionDenied


def is_not_blocked(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        prefix = getattr(self, 'counter_prefix')
        phone = getattr(self, 'phone')
        max_tries = int(getattr(self, 'max_tries'))
        counter = cache.get(prefix + phone, None)
        if counter and int(counter) > (max_tries - 1):
            raise PermissionDenied(detail=f"Number {phone} is blocked!")
        return func(self, *args, **kwargs)

    return wrapper

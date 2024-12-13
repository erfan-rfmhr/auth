from functools import wraps

from rest_framework.exceptions import PermissionDenied


def is_not_blocked(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.is_blocked():
            raise PermissionDenied
        return func(self, *args, **kwargs)

    return wrapper

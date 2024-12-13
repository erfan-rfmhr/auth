from abc import ABC, abstractmethod

from django.conf import settings
from django.core.cache import cache


class AbstractVerificationService(ABC):
    max_value = None
    min_value = None
    key_prefix = None
    counter_prefix = None
    max_tries = None
    timout = None

    def __init__(self, phone: str):
        self.phone = phone

    @classmethod
    @abstractmethod
    def validate(cls, otp: int):
        raise NotImplementedError

    @abstractmethod
    def is_verified(self, otp: int) -> bool:
        raise NotImplementedError

    def expire(self):
        self.expire_key()
        self.expire_counter()

    def expire_key(self):
        cache.delete(self.key_prefix + self.phone)

    def expire_counter(self):
        cache.delete(self.counter_prefix + self.phone)

    def increment_block_counter(self):
        count = cache.get(self.counter_prefix + self.phone, None)
        if count is None:
            cache.set(self.counter_prefix + self.phone, 1, settings.OTP_TIMEOUT)
        else:
            cache.set(self.counter_prefix + self.phone, count + 1, settings.OTP_TIMEOUT)

    def is_blocked(self) -> bool:
        prefix = self.counter_prefix
        phone = self.phone
        max_tries = int(self.max_tries)
        counter = cache.get(prefix + phone, None)
        if counter and int(counter) > (max_tries - 1):
            return True
        return False

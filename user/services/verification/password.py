import random

from django.conf import settings
from django.core.cache import cache
from rest_framework import serializers

from user.services.decorators import is_not_blocked
from user.services.verification.abstract import AbstractVerificationService


class PasswordService(AbstractVerificationService):
    counter_prefix = settings.PASSWORD_COUNTER_PREFIX
    max_tries = settings.MAX_AUTHENTICATION_TRIES
    timout = settings.PASSWORD_TIMEOUT

    @classmethod
    def validate(cls, otp: int):
        if not cls.min_value <= otp <= cls.max_value:
            raise serializers.ValidationError(f"OTP number must be between {cls.min_value} and {cls.max_value}")

    @is_not_blocked
    def is_verified(self, otp: int) -> bool:
        cached_otp = cache.get(self.key_prefix + self.phone, None)
        if not (bool(cached_otp) and (otp == int(cached_otp))):
            self.increment_block_counter()
            return False
        return True

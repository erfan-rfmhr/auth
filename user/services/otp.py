import random

from django.conf import settings
from django.core.cache import cache
from rest_framework import serializers

from user.services.decorators import is_not_blocked


class OTPService:
    max_value = settings.OTP_MAX_VALUE
    min_value = settings.OTP_MIN_VALUE
    key_prefix = settings.OTP_KEY_PREFIX
    counter_prefix = settings.OTP_COUNTER_PREFIX
    max_tries = settings.MAX_AUTHENTICATION_TRIES

    def __init__(self, phone: str):
        self.phone = phone

    @classmethod
    def _generate_random_otp(cls) -> int:
        return random.randint(int(cls.min_value), int(cls.max_value))

    @is_not_blocked
    def send_otp_sms(self, message=None) -> int:
        """
        :param message: in a real app this is the real sms message
        :return: otp number
        """
        key = self.key_prefix + self.phone
        otp = self._generate_random_otp()
        cache.set(key, otp, settings.OTP_TIMEOUT)
        return otp

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

    def expire(self):
        cache.delete(self.key_prefix + self.phone)
        cache.delete(self.counter_prefix + self.phone)

    def increment_block_counter(self):
        count = cache.get(self.counter_prefix + self.phone, None)
        if count is None:
            cache.set(self.counter_prefix + self.phone, 1, settings.OTP_TIMEOUT)
        else:
            cache.set(self.counter_prefix + self.phone, count + 1, settings.OTP_TIMEOUT)

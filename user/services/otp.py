import random

from django.conf import settings
from django.core.cache import cache


class OTPService:
    max_value = settings.OTP_MAX_VALUE
    min_value = settings.OTP_MIN_VALUE
    key_prefix = settings.OTP_KEY_PREFIX

    @classmethod
    def _generate_random_otp(cls) -> int:
        return random.randint(int(cls.min_value), int(cls.max_value))

    @classmethod
    def send_otp_sms(cls, phone: str, message=None) -> int:
        """
        :param phone: user phone number
        :param message: in a real app this is the real sms message
        :return: otp number
        """
        key = cls.key_prefix + phone
        otp = cls._generate_random_otp()
        cache.set(key, otp, settings.OTP_TIMEOUT)
        print(otp)
        return otp

    @classmethod
    def validate(cls, otp: int) -> bool:
        return cls.min_value <= otp <= cls.max_value

    @classmethod
    def is_verified(cls, otp: int, phone: str) -> bool:
        cached_otp = cache.get(cls.key_prefix + phone, None)
        return bool(cached_otp) and (otp == int(cached_otp))

    @classmethod
    def expire(cls, phone: str):
        cache.delete(cls.key_prefix + phone)

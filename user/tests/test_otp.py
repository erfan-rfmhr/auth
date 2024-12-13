from unittest.mock import patch

from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse

from user.models import User
from user.services.verification.otp import OTPService
from user.tests.abstract_test_suit import AbstractTestSuite

TEST_OTP = 102_000
COUNTER = 0


def get_test_otp(*args, **kwargs):
    return TEST_OTP


def get_cache(*args, **kwargs):
    global COUNTER
    prefix = args[0]
    if "otp_counter_" in prefix:
        return COUNTER
    elif "otp_" in prefix:
        return TEST_OTP


def set_cache(*args, **kwargs):
    global COUNTER
    prefix = args[0]
    if "counter" in prefix:
        COUNTER += 1


class TestOTP(AbstractTestSuite):
    def tearDown(self):
        global COUNTER
        super().tearDown()
        COUNTER = 0

    def test_otp_for_existed_user(self):
        self.client.post(reverse("user:register"), data={"phone": self.user1.username})
        # user exists so any otp must be invalid
        response = self.client.post(
            reverse("user:otp_verification"),
            data={"phone": self.user1.username, "otp": "123764"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "invalid otp"
                ]
            }
        )

    @patch.object(OTPService, "_generate_random_otp", side_effect=get_test_otp)
    @patch("django.core.cache.cache.get", side_effect=get_cache)
    def test_otp_for_new_user(self, *args, **kwargs):
        response = self.client.post(reverse("user:register"), data={"phone": self.user2.username})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(User.objects.filter(username=self.user2.username).exists())

    @patch.object(OTPService, "_generate_random_otp", side_effect=get_test_otp)
    @patch("django.core.cache.cache.get", side_effect=get_cache)
    @patch("django.core.cache.cache.set", side_effect=set_cache)
    def test_block_otp(self, *args):
        service = OTPService(self.user2.username)
        self.client.post(reverse("user:register"), data={"phone": self.user2.username})
        for _ in range(settings.MAX_AUTHENTICATION_TRIES):
            self.client.post(
                reverse("user:otp_verification"),
                data={"phone": self.user2.username, "otp": "100_000"}
            )
        self.assertTrue(service.is_blocked())

from unittest.mock import patch

from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse

from user.services.verification.password import PasswordService
from user.tests.abstract_test_suit import AbstractTestSuite

COUNTER = 0


def get_cache(*args, **kwargs):
    global COUNTER
    prefix = args[0]
    if "counter" in prefix:
        return COUNTER


def set_cache(*args, **kwargs):
    global COUNTER
    prefix = args[0]
    if "counter" in prefix:
        COUNTER += 1


class TestPassword(AbstractTestSuite):
    def tearDown(self):
        global COUNTER
        super().tearDown()
        COUNTER = 0

    def test_password_for_existed_user(self):
        self.client.post(reverse("user:register"), data={"phone": self.user3.username})
        response = self.client.post(
            reverse("user:password_verification"),
            data={"username": self.user3.username, "password": "123764"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Password is invalid."
                ]
            }
        )

    @patch("django.core.cache.cache.get", side_effect=get_cache)
    @patch("django.core.cache.cache.set", side_effect=set_cache)
    def test_block_password(self, *args):
        service = PasswordService(self.user3.username)
        self.client.post(reverse("user:register"), data={"phone": self.user3.username})
        for _ in range(settings.MAX_AUTHENTICATION_TRIES):
            self.client.post(
                reverse("user:password_verification"),
                data={"username": self.user2.username, "password": "1234"}
            )
        self.assertTrue(service.is_blocked())

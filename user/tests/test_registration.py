from rest_framework import status
from rest_framework.reverse import reverse

from user.tests.abstract_test_suit import AbstractTestSuite


class TestRegistration(AbstractTestSuite):
    def test_registration_url(self):
        response1 = self.client.post(reverse("user:register"), data={"phone": self.user1.username})
        response2 = self.client.post(reverse("user:register"), data={"phone": self.user2.username})

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        password_verification_url = "http://testserver" + reverse("user:password_verification")
        expected_response1 = {"registration_url": password_verification_url}

        otp_registration_url = "http://testserver" + reverse("user:otp_verification")
        expected_response2 = {"registration_url": otp_registration_url}

        self.assertEqual(response1.json(), expected_response1)
        self.assertEqual(response2.json(), expected_response2)

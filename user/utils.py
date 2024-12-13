from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.reverse import reverse

from user.services.otp import OTPService

User = get_user_model()


def get_registration_url(phone: str, request: Request) -> str:
    if User.objects.filter(username=phone).exists():
        return request.build_absolute_uri(reverse("user:password_verification"))
    OTPService(phone).send_otp_sms()
    return request.build_absolute_uri(reverse("user:otp_verification"))

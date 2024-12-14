from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, PasswordField

from user.api.fields import PhoneField
from user.services.verification.otp import OTPService
from user.services.verification.password import PasswordService

User = get_user_model()


class OTPJWTSerializer(TokenObtainPairSerializer):
    phone = PhoneField(required=True)
    otp = serializers.IntegerField(required=True, validators=[OTPService.validate])

    def __init__(self, instance=None, data=empty, **kwargs):
        serializers.BaseSerializer.__init__(self, instance, data, **kwargs)

    def validate(self, attrs):
        phone = attrs.get('phone')
        otp = attrs.get('otp')
        service = OTPService(phone)
        if not service.is_verified(otp):
            raise serializers.ValidationError("invalid otp")
        service.expire()
        user, _ = User.objects.get_or_create(username=phone)
        token = self.get_token(user)

        return {
            "access": str(token.access_token),
            "refresh": str(token),
        }


class PasswordJWTSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "invalid_password": "Password is invalid.",
        "blocked_number": "Phone number is blocked.",
    }
    service_class = PasswordService

    phone = PhoneField(required=True, source="username")

    def __init__(self, instance=None, data=empty, **kwargs):
        serializers.BaseSerializer.__init__(self, instance, data, **kwargs)
        self.fields["password"] = PasswordField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        service = self.service_class(username)
        blocked = service.is_blocked()
        if blocked:
            self.fail("blocked_number")
        user = authenticate(username=username, password=password)
        if not user:
            code = "blocked_number" if blocked else "invalid_password"
            service.increment_block_counter()
            raise self.fail(code)
        service.expire_counter()
        token = self.get_token(user)

        return {
            "access": str(token.access_token),
            "refresh": str(token),
        }

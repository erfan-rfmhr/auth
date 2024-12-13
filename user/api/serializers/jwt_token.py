from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.api.fields import PhoneField
from user.services.otp import OTPService

User = get_user_model()


class OTPJWTSerializer(TokenObtainPairSerializer):
    phone = PhoneField(required=True)
    otp = serializers.IntegerField(required=True, validators=[OTPService.validate])

    def __init__(self, instance=None, data=empty, **kwargs):
        serializers.BaseSerializer.__init__(self, instance, data, **kwargs)

    def validate(self, attrs):
        phone = attrs.get('phone')
        otp = attrs.get('otp')
        if not OTPService.is_verified(otp, phone):
            raise serializers.ValidationError("invalid otp")
        OTPService.expire(phone)
        user, _ = User.objects.get_or_create(username=phone)
        token = self.get_token(user)

        return {
            "access": str(token.access_token),
            "refresh": str(token),
        }

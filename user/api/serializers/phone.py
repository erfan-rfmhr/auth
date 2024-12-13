from rest_framework import serializers

from user.api.fields import PhoneField


class PhoneVerificationSerializer(serializers.Serializer):
    phone = PhoneField(required=True)

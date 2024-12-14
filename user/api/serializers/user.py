from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.api.fields import PhoneField


class UserSerializer(serializers.ModelSerializer):
    phone = PhoneField(required=True, source="username")

    class Meta:
        model = get_user_model()
        fields = ["id", "phone", "email", "first_name", "last_name"]
        read_only_fields = ["id", "phone"]

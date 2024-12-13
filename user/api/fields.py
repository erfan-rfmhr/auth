import re

from django.core.validators import RegexValidator
from rest_framework import serializers


class PhoneField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs["validators"] = [
            RegexValidator(
                regex=r"^(09\d{9}|\+989\d{9})$",
                message="شماره تلفن همراه باید بین 11 تا 13 کاراکتر باشد و باید با صفر یا +98 شروع شود.",
            )
        ]
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if re.match(r"^0\d{10}$", data):
            data = "+98" + data[1:]
        return super().to_internal_value(data)

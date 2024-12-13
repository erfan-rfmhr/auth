import re

from django.core.validators import RegexValidator
from django.db.models import CharField
from persian import convert_fa_numbers

mobile_phone_regex = RegexValidator(
    regex=r"^(98|\+98|0)?(9\d{9}$)",
)


def format_country_code_phone(value):
    if value:
        value = convert_fa_numbers(value)
        if value.startswith("0"):
            return re.sub(r"^0", "+98", value)
        if (len(value) == 10 and value.startswith("9")) or len(value.lstrip("0")) == 8:
            return f"+98{value}"
        if len(value) == 12 and value.startswith("98"):
            return f"+{value}"
    return value


class PhoneField(CharField):
    def to_python(self, value):
        value = super().to_python(value)
        return format_country_code_phone(value)

    def __init__(self, max_length=13, *args, **kwargs):
        super().__init__(*args, max_length=max_length, **kwargs)
        self.validators.append(mobile_phone_regex)

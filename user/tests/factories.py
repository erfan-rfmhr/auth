import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "12345")

    @factory.lazy_attribute
    def username(self) -> str:
        from faker import Faker

        fake = Faker("fa_IR")
        return "+989" + "".join(fake.msisdn()[4:])

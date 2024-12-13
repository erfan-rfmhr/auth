from django.contrib.auth.models import AbstractUser

from user.models.fields import PhoneField


class User(AbstractUser):
    username = PhoneField(unique=True, db_index=True)

    def __str__(self):
        return self.username

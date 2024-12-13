from unittest.mock import patch

from django.core.cache import cache
from rest_framework.test import APITransactionTestCase

from user.models import User
from user.tests.factories import UserFactory


class AbstractTestSuite(APITransactionTestCase):
    def setUp(self):
        self.client = self.client_class()
        self.user1 = UserFactory(username="+989121092055")
        self.user2 = User(username="+989121092054")
        self.user3 = UserFactory(username="+989121092053", password="<PASSWORD>")
        cache.clear()

import datetime
from django.utils import timezone

from django.test import TestCase
from accounts.models import User

# Model Tests
class UserModelTest(TestCase):
    def setUp(self):
        User.objects.create(
            email="test@example.com",
            password="test"
        )

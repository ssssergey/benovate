from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import DataError

from client.models import Client


class ClientModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@test.com', password='123456')

    def test_add_client(self):
        """
        Successfully create client
        """
        Client.objects.create(user=self.user, inn='123456789000', account=34.3)
        self.assertEquals(Client.objects.count(), 1)

    def test_inn_validation(self):
        # Non-numeric value
        with self.assertRaises(ValidationError) as e:
            Client.objects.create(user=self.user, inn='aaaa1111111', account=34.3)

        # Too long value
        with self.assertRaises(DataError) as e:
            Client.objects.create(user=self.user, inn='123456789000000000', account=34.3)
from django.test import TestCase

from django.contrib.auth.models import User

from client.models import Client


class ClientListSerializerTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='test1', email='test1@test.com',
                                              password='123456', first_name='John', last_name='Doe')
        self.client1 = Client.objects.create(id=1, user=self.user1, inn='1111111111', account=10)
        self.user2 = User.objects.create_user(username='test2', email='test2@test.com',
                                              password='123456', first_name='Alex', last_name='Doe')
        self.client2 = Client.objects.create(id=2, user=self.user2, inn='2222222222', account=10)
        self.user3 = User.objects.create_user(username='test3', email='test3@test.com',
                                              password='123456', first_name='Bob', last_name='Doe')
        self.client3 = Client.objects.create(id=3, user=self.user3, inn='3333333333', account=10)

    def test_list(self):
        from ..serializers import ClientListSerializer
        clients = Client.objects.all()
        serializer = ClientListSerializer(clients, many=True)
        self.assertEqual(len(serializer.data), 3)
        self.assertEqual(serializer.data[0]['id'], 1)
        self.assertEqual(serializer.data[0]['fullname'], 'John Doe')

    def test_update(self):
        from ..serializers import ClientUpdateSerializer
        # Test validation
        serializer = ClientUpdateSerializer(self.client1, data={'inns': '2222222222', 'amount': 10})
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)

        serializer = ClientUpdateSerializer(self.client1, data={'inns': '', 'amount': 100})
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)
        self.assertEqual(serializer.errors['inns'], ['Это поле не может быть пустым.'])
        self.assertEqual(serializer.errors['amount'], ['Сумма 100.00 превышает текущий баланс клиента John Doe'])

        serializer = ClientUpdateSerializer(self.client1, data={'inns': '5555555555', 'amount': 's'})
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)
        self.assertEqual(serializer.errors['inns'], ['Данные номера ИНН не найдены: 5555555555'])
        self.assertEqual(serializer.errors['amount'], ['Требуется численное значение.'])

        # Test update method
        serializer = ClientUpdateSerializer(self.client1, data={'inns': '2222222222, 3333333333', 'amount': 10})
        serializer.is_valid()
        serializer.save()
        self.client1.refresh_from_db()
        self.client2.refresh_from_db()
        self.client3.refresh_from_db()
        self.assertEqual(self.client1.account, 0)
        self.assertEqual(self.client2.account, 15)
        self.assertEqual(self.client3.account, 15)

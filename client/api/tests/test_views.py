from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from client.models import Client


class ClientAPITestCase(APITestCase):
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
        response = self.client.get(reverse('api:clients_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['fullname'], 'John Doe')

    def test_update(self):
        response = self.client.put(reverse('api:clients_update', args=(1,)),
                                   data={'inns': '2222222222, 3333333333', 'amount': 10})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['account'], 0)
        self.assertEqual(response.data['fullname'], 'John Doe')
        self.client1.refresh_from_db()
        self.client2.refresh_from_db()
        self.client3.refresh_from_db()
        self.assertEqual(self.client1.account, 0)
        self.assertEqual(self.client2.account, 15)
        self.assertEqual(self.client3.account, 15)

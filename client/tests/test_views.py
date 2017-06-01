from django.test import TestCase, Client
from django.urls import reverse


class IndexViewTestCase(TestCase):
    def test_view(self):
        c = Client()
        response = c.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Тестовое задание', response.content.decode())

from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from .models import User


class AuthTest(APITestCase):
    """Тесты для авторизации и регистрации."""

    register_url = reverse_lazy('users:register')
    login_url = reverse_lazy('users:login')

    def setUp(self):
        self.email = "maria_lepilina1@mail.ru"
        self.password = "mar12345"

        self.register_payload = {
            "email": self.email,
            "name": "Maria",
            "surname": "L",
            "phone": 89500000002,
            "password": self.password
        }

    def test_register(self):
        """Тестируем регистрацию."""
        self.assertFalse(User.objects.all().exists())
        response = self.client.post(self.register_url, data=self.register_payload)
        self.assertEqual(response.status_code, 201)

        new_user = User.objects.get(email=self.email)
        self.assert_(new_user)

    def test_login(self):
        """Тестируем авторизацию."""
        new_user = User.objects.create(**self.register_payload)
        new_user.set_password(self.password)
        new_user.save()

        payload = {
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(self.login_url, data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)


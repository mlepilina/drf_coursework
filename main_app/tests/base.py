from rest_framework.test import APITestCase

from auth_app.models import User


class BaseMainTest(APITestCase):
    """Тесты привычек."""

    def create_test_user(self):
        email = "maria_lepilina1@mail.ru"
        password = "mar12345"

        register_payload = {
            "email": email,
            "name": "Maria",
            "surname": "L",
            "phone": 89500000002,
            "password": password
        }

        new_user = User.objects.create(**register_payload)
        new_user.set_password(password)
        new_user.save()

        return new_user

    def setUp(self):
        self.user = self.create_test_user()
        self.client.force_authenticate(self.user)

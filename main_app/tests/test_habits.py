from django.urls import reverse_lazy

from main_app.tests.base import BaseMainTest
from main_app.models import Habit


class AuthTest(BaseMainTest):
    """Тесты привычек."""

    def test_create_habbit(self):
        """Тестируем создание привычки."""
        url = reverse_lazy('main_app:habit')
        payload = {
            "action": "Полезное действие",
            "place": "Полезное место",
            "time": "17:46:42:000000",
            "habit_type": Habit.HabitType.USEFUL,
            "periodicity": [5],
            "reward": '',
            "time_to_complete": 120,
            "publicity": Habit.Publicity.PUBLIC
        }

        self.assertFalse(Habit.objects.all().exists())

        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, 201)
        self.assertTrue('id' in response.data)
        new_habit = Habit.objects.get(id=response.data['id'])
        self.assert_(new_habit)

    def test_create_habbit_validations(self):
        """Тестируем валидацию при создании привычки."""

        url = reverse_lazy('main_app:habit')
        payload = {
            "action": "Полезное действие",
            "place": "Полезное место",
            "time": "17:46:42:000000",
            "habit_type": Habit.HabitType.PLEASANT,
            "periodicity": [5],
            "reward": '',
            "time_to_complete": 120,
            "publicity": Habit.Publicity.PUBLIC
        }

        payload_1 = payload.copy()
        payload_1['reward'] = 'Что-то'
        self.assertFalse(Habit.objects.all().exists())
        response = self.client.post(url, data=payload_1)
        self.assertEqual(response.status_code, 400)

        payload_2 = payload.copy()
        payload_2['periodicity'] = [1, 2, 3, 4, 5, 6, 7, 8]
        response = self.client.post(url, data=payload_2)
        self.assertEqual(response.status_code, 400)

        payload_3 = payload.copy()
        payload_3['time_to_complete'] = 121
        response = self.client.post(url, data=payload_3)
        self.assertEqual(response.status_code, 400)

    def test_update_habbit(self):
        """Тестируем редактирование привычки."""

        payload = {
            "action": "Полезное действие",
            "place": "Полезное место",
            "time": "17:46:42:000000",
            "habit_type": Habit.HabitType.PLEASANT,
            "periodicity": [5],
            "reward": '',
            "time_to_complete": 120,
            "publicity": Habit.Publicity.PUBLIC,
            'user': self.user
        }
        habit = Habit.objects.create(**payload)
        url = reverse_lazy('main_app:connection_create', kwargs={'habit_id': habit.id})
        response = self.client.patch(url, data={'action': 'смотреть в стену'})
        self.assertEqual(response.status_code, 200)

        habit.refresh_from_db()
        self.assertEqual(habit.action, 'смотреть в стену')

    def test_relate_habbits(self):
        """Тестируем связывание привычек."""
        plesant_payload = {
            "action": "Полезное действие",
            "place": "Полезное место",
            "time": "17:46:42:000000",
            "habit_type": Habit.HabitType.PLEASANT,
            "periodicity": [5],
            "reward": '',
            "time_to_complete": 120,
            "publicity": Habit.Publicity.PUBLIC,
            'user': self.user
        }
        useful_payload = plesant_payload.copy()
        useful_payload['habit_type'] = Habit.HabitType.USEFUL
        plesant_habit = Habit.objects.create(**plesant_payload)
        useful_habit = Habit.objects.create(**useful_payload)
        url = reverse_lazy('main_app:connection_create', kwargs={'habit_id': useful_habit.id})
        response = self.client.post(url, data={'id': plesant_habit.id})
        self.assertEqual(response.status_code, 201)

    def test_delete_habbit(self):
        """Тестируем удаление привычки."""
        payload = {
            "action": "Полезное действие",
            "place": "Полезное место",
            "time": "17:46:42:000000",
            "habit_type": Habit.HabitType.PLEASANT,
            "periodicity": [5],
            "reward": '',
            "time_to_complete": 120,
            "publicity": Habit.Publicity.PUBLIC,
            'user': self.user
        }
        habit = Habit.objects.create(**payload)
        url = reverse_lazy('main_app:connection_create', kwargs={'habit_id': habit.id})
        response = self.client.delete(url, data={'action': 'смотреть в стену'})
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Habit.objects.filter(id=habit.id).exists())

    def test_get_habbits(self):
        """Тестируем получение привычек пользователя."""
        payload = {
            "action": "Полезное действие",
            "place": "Полезное место",
            "time": "17:46:42:000000",
            "habit_type": Habit.HabitType.PLEASANT,
            "periodicity": [5],
            "reward": '',
            "time_to_complete": 120,
            "publicity": Habit.Publicity.PUBLIC,
            'user': self.user
        }
        habit = Habit.objects.create(**payload)
        url = reverse_lazy('main_app:habit')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for key in ['list', 'current_page', 'next_page', 'previous_page']:
            self.assertTrue(key in response.data)

        self.assertEqual(response.data['list'][0]['action'], payload['action'])

    def test_get_public_habbits(self):
        """Тестируем получение публичных привычек."""

        payload = {
            "action": "Полезное действие",
            "place": "Полезное место",
            "time": "17:46:42:000000",
            "habit_type": Habit.HabitType.PLEASANT,
            "periodicity": [5],
            "reward": '',
            "time_to_complete": 120,
            "publicity": Habit.Publicity.PUBLIC,
            'user': self.user
        }

        payload_2 = payload.copy()
        payload_2['publicity'] = Habit.Publicity.PRIVATE
        for data in payload, payload_2:
            Habit.objects.create(**data)

        url = reverse_lazy('main_app:habits_public')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for key in ['list', 'current_page', 'next_page', 'previous_page']:
            self.assertTrue(key in response.data)

        self.assertEqual(len(response.data['list']), 1)
        self.assertEqual(response.data['list'][0]['action'], payload['action'])

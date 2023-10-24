from rest_framework import serializers

from main_app.models import Habit, HabitsConnection
from main_app.validators import RewardValidator


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = [
            'action',
            'place',
            'time',
            'habit_type',
            'periodicity',
            'reward',
            'time_to_complete',
            'publicity',
        ]
        validators = [
            RewardValidator(habit_type='habit_type', reward='reward'),
        ]

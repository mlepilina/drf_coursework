from rest_framework import serializers

from main_app.models import Habit, HabitsConnection
from main_app.validators import RewardValidator


class HabitSerializer(serializers.ModelSerializer):

    related_habits = serializers.SerializerMethodField(method_name='get_related_habits')

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
            'related_habits'
        ]
        validators = [
            RewardValidator(habit_type='habit_type', reward='reward'),
        ]

    def get_related_habits(self, habit: Habit):
        if habit.habit_type == Habit.HabitType.USEFUL:
            query = habit.link_usefuls.all().values_list('pleasant__action', flat=True)
        else:
            query = habit.link_pleasants.all().values_list('useful__action', flat=True)

        return list(query)

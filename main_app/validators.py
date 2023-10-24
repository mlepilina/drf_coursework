from rest_framework.validators import ValidationError


class RewardValidator:
    def __init__(self, habit_type, reward):
        self.field_habit_type = habit_type
        self.field_reward = reward

    def __call__(self, value):
        habit_field_value = value.get(self.field_habit_type)
        reward_field_value = value.get(self.field_reward)
        if habit_field_value == 'pleasant' and reward_field_value is not None:
            raise ValidationError("Невозможно установить вознаграждение в приятной привычке")

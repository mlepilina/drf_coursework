from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator, MinLengthValidator

from django.db import models

from auth_app.models import User

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):

    class HabitType(models.TextChoices):
        PLEASANT = ('pleasant', 'приятная')
        USEFUL = ('useful', 'полезная')

    class Publicity(models.TextChoices):
        PUBLIC = ('public', 'публичная')
        PRIVATE = ('private', 'приватная')

    action = models.CharField(max_length=200, verbose_name='действие привычки')
    place = models.CharField(max_length=100, verbose_name='место')
    time = models.TimeField(verbose_name='время')
    habit_type = models.CharField(max_length=50, choices=HabitType.choices, verbose_name='тип привычки')
    periodicity = ArrayField(
        base_field=models.IntegerField(),
        size=7,
        default=list,
        validators=[MaxLengthValidator(7), MinLengthValidator(1)],
        verbose_name='периодичность (в днях недели)'
    )
    reward = models.CharField(max_length=200, verbose_name='вознаграждение', **NULLABLE)
    time_to_complete = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(120), MinValueValidator(1)],
        verbose_name='время выполнения (сек)'
    )
    publicity = models.CharField(max_length=50, choices=Publicity.choices, verbose_name='публичность')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', related_name='habits')

    def __str__(self):
        return f'{self.action}. Пользователь: {self.user}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'


class HabitsConnection(models.Model):

    useful = models.ForeignKey(Habit, related_name='link_usefuls', on_delete=models.CASCADE, verbose_name='полезная привычка')
    pleasant = models.ForeignKey(Habit, related_name='link_pleasants', on_delete=models.CASCADE, verbose_name='приятная привычка')

    def __str__(self):
        return f'{self.useful}{self.pleasant}'

    class Meta:
        verbose_name = 'связанная привычка'
        verbose_name_plural = 'связанные привычки'


class Notice(models.Model):

    class SendingType(models.TextChoices):
        EMAIL = ('email', 'по почте')
        TELEGRAM = ('telegram', 'в телеграм')

    sending_time = models.DateTimeField(verbose_name='время отправки уведомления')
    text = models.TextField(verbose_name='текст уведомления')
    sending_type = models.CharField(max_length=50, choices=SendingType.choices, verbose_name='тип отправки')

    habit = models.ForeignKey(Habit, related_name='notifications', on_delete=models.CASCADE, verbose_name='привычка')

    def __str__(self):
        return f'{self.habit} {self.sending_type} {self.sending_time}'

    class Meta:
        verbose_name = 'уведомление'
        verbose_name_plural = 'уведомления'


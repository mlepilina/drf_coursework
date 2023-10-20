from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):

    username = None

    email = models.EmailField(verbose_name='контактный email', unique=True)
    surname = models.CharField(max_length=100, verbose_name='фамилия')
    name = models.CharField(max_length=100, verbose_name='имя')
    phone = models.PositiveBigIntegerField(verbose_name='номер телефона', unique=True)
    nickname = models.CharField(max_length=100, verbose_name='никнейм в телеграм', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


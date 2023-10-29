from datetime import datetime, timedelta

import requests
from django.conf import settings
from django.core.mail import send_mail

from config.celery import app
from main_app.models import Habit, Notice


@app.task
def create_notification():
    now = datetime.now()
    time_now = now.time()
    time_10_min = (now + timedelta(minutes=10)).time()
    today_start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
    habits_list = Habit.objects.filter(
        periodicity__contains=[datetime.isoweekday(now)],
        time__range=(time_now, time_10_min)
    )
    for habit in habits_list:

        today_sent_notices = habit.notifications.filter(
            sending_time__lte=now,
            sending_type__gte=today_start_time
        ).exists()

        if not today_sent_notices:
            send_message(habit.id)


@app.task
def send_message(habit_id):
    habit = Habit.objects.get(id=habit_id)
    user = habit.user

    text = f"Пора выполнить привычку: {habit.action} сегодня в {habit.time}"

    if user.chat_id:
        # Если есть айди чата в телеграме
        url = f"https://api.telegram.org/{settings.TELEGRAM_TOKEN}/sendMessage"
        requests.get(url, params={'chat_id': user.chat_id, 'text': text})
        sending_type = Notice.SendingType.TELEGRAM
    else:
        # Иначе отправляем на почту
        send_mail(
            subject='Напоминание о привычке',
            message=text,
            recipient_list=[user.email],
            from_email=settings.EMAIL_HOST_USER
        )
        sending_type = Notice.SendingType.EMAIL

    Notice.objects.create(
        sending_time=datetime.now(),
        text=text,
        sending_type=sending_type,
        habit=habit,
    )

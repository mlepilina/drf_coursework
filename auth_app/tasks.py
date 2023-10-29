from config.celery import app

from django.conf import settings
from django.core.mail import send_mail


@app.task
def send_mail_task(email, name):
    """
    Запуск сразу: send_mail_task.delay()
    Отложенный запуск: send_mail_task.apply_async(args=(), countdown=15)
    """
    send_mail(
        subject='Поздравляем с регистрацией',
        message=f'Здравствуйте, {name}! Вы зарегистрированы на сайте трекера привычек!',
        recipient_list=[email],
        from_email=settings.EMAIL_HOST_USER
    )
    print('Письмо отправлено')

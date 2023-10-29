# drf_coursework
Курсовая работа по DRF

## Запуск приложения

```shell
python manage.py runserver
```


## Запуск Celery

```shell
celery -A config worker -l DEBUG -P eventlet
```


## Запуск Beat
```shell
celery -A config beat -l info
```

## Работа с Telegram
для корректной работы с телеграмом необходимо установить токен бота в переменную окружения `TELEGRAM_TOKEN`

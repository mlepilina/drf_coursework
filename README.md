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


## Авторизация

Для авторизации необходимо получить пару JWT-access и refresh токенов на эндпоинте `POST: /auth/login/`

Далее каждый эндпоинт, кроме регистрации будет требовать передачи access-токена в заголовках.

### Пример заголовка авторизации:

```
Authorization: Bearer <access_token>
```

## Запуск Docker

Создайте файл .env на основе примера .env.example, заполните его корректными значениями. 

Для запуска наберите команду:

```shell
docker-compose up --build
```
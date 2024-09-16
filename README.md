**LMS-система онлайн обучения**

**Описание**
LMS-система онлайн обучения представляет собой API для управления Курсами и уроками.

**Функционал**
- Редактирование профиля пользователя
- Создание, редактирование и удаление курсов
- Создание, редактирование и удаление уроков
- Ведение учета платежей от пользователей
- Подписка, отписка от курсов
- Оплата курса

**Фоновый функционал**
- Отправка уведомления по электронной почты об изменении курса (урока)
- Деактивация учетной записи пользователя без активности более месяца

**Технологический стек**
- Python 3.x
- Django
- Django-Rest
- PostgreSQL
- stripe
- celery
- redis
- django-celery-beat
- docker
- docker-compose

**Дополнительные требования**
- Наличие учетной записи почтового сервиса
- Наличие учетной записи сервиса приема платежей Stripe

**Установка**
Для запуска проекта локально, выполните следующие шаги:

1. **Клонирование репозитория:**
    ```bash
    git clone https://github.com/KudryashovR/online_training.git
    cd online_training
    ```

2. **Создание и настройка файла `.env`:**
    Создайте файл `.env` в корне проекта и добавьте настройки, указанные в файле `.env.example`

3. **Сборка образа и запуск в фоне после успешной сборки**
   ```bash
   docker-compose up -d —build
   ```

4. **Создание суперпользователя**
   ```bash
   docker exec -it web poetry run python manage.py createsuperuser
   ```

**Использование**
Доступные URL:
- /api/courses/
- /api/lessons/
- /api/users/profile/
- /api/users/payments/
- /api/subscribe/
- /api/create-payment/
- /api/check-session-status/
- /users/users/
- /api/users/token/
- /api/users/token/refresh/
- /api/users/register/

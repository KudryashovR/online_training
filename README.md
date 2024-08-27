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
- django-celery-beat = "^2.7.0"

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

2. **Настройка виртуального окружения и установка зависимостей:**
    ```bash
    python poetry install
    python poetry shell
    ```

3. **Создание и настройка файла `.env`:**
    Создайте файл `.env` в корне проекта и добавьте настройки, указанные в файле `.env.example`

4. **Применение миграций и запуск сервера:**
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

5. **Запуск служб контроля выполнения фоновых задач:**
    ```bash
    celery -A config worker -l INFO
    celery -A config beat -l INFO
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

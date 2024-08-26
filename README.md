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

**Технологический стек**
- Python 3.x
- Django
- Django-Rest
- PostgreSQL

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

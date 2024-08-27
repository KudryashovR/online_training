from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

from config import settings

User = get_user_model()


@shared_task
def send_update_email(user_email, course_name):
    """
    Отправляет электронное письмо пользователю с уведомлением об обновлении курса.

    Параметры:
    user_email (str): Адрес электронной почты пользователя, которому нужно отправить уведомление.
    course_name (str): Название курса, который был обновлен.

    Функция использует настройки электронной почты из Django settings для отправки сообщения.
    Электронное письмо содержит информацию о том, что курс был обновлен и призывает пользователя проверить новые
    материалы.
    """

    send_mail(
        f'Курс обновлен: {course_name}',
        f'Уважаемый пользователь, курс "{course_name}" был обновлен. Проверьте новые материалы!',
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )


@shared_task
def deactivate_inactive_users():
    """
    Деактивирует неактивных пользователей, которые не входили в систему более 30 дней, и отправляет им письмо
    уведомление.

    Функция выбирает всех пользователей, которые были активны, но последний раз
    входили в систему более месяца назад, и деактивирует их, устанавливая
    флаг is_active в False.

    Для каждого деактивированного пользователя отправляется письмо уведомление с указанием,
    что их учетная запись была деактивирована, а также рекомендациями по восстановлению доступа.

    Заметки:
    - Используется временной период в 30 дней для определения неактивности.
    - Отправка почты осуществляется с использованием настроек электронной почты из settings.

    Важно:
    - Прежде чем применять эту функцию, убедитесь, что неактивных пользователей необходимо
      деактивировать с точки зрения бизнес-логики вашего приложения.
    """

    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)

    for user in inactive_users:
        user.is_active = False
        send_mail(
            f'Деактивация учетной записи',
            f'Уважаемый пользователь, Ваша учетная запись деактивирована! Для восстановления доступа свяжитесь с администратором.',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        user.save()

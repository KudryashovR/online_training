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
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()

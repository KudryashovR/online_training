from celery import shared_task
from django.core.mail import send_mail

from config import settings


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

from celery import shared_task
from django.core.mail import send_mail

from config import settings


@shared_task
def send_update_email(user_email, course_name):
    send_mail(
        f'Курс обновлен: {course_name}',
        f'Уважаемый пользователь, курс "{course_name}" был обновлен. Проверьте новые материалы!',
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )

from django.core.management import BaseCommand

from lms.models import Course, Lesson
from users.models import CustomUser, Payment


class Command(BaseCommand):
    help = 'Записывает тестовые данные о платежах в базу данных'

    def handle(self, *args, **kwargs):
        try:
            user1 = CustomUser.objects.get(pk=1)
        except CustomUser.DoesNotExist:
            user1 = CustomUser.objects.create(pk=1, email='testuser1@example.com', password='testpassword')

            self.stdout.write(self.style.WARNING('Создан тестовый пользователь с pk=1'))

        try:
            user2 = CustomUser.objects.get(pk=2)
        except CustomUser.DoesNotExist:
            user2 = CustomUser.objects.create(pk=2, email='testuser2@example.com', password='testpassword')

            self.stdout.write(self.style.WARNING('Создан тестовый пользователь с pk=2'))

        try:
            course = Course.objects.get(pk=1)
        except Course.DoesNotExist:
            course = Course.objects.create(pk=1, title='Test Course', description='This is a test course.')

            self.stdout.write(self.style.WARNING('Создан тестовый курс с pk=1'))

        try:
            lesson = Lesson.objects.get(pk=1)
        except Lesson.DoesNotExist:
            lesson = Lesson.objects.create(pk=1, title='Test Lesson', content='This is a test lesson.')
            self.stdout.write(self.style.WARNING('Создан тестовый урок с pk=1'))

        Payment.objects.create(
            user=user1,
            paid_course=course,
            amount=199.99,
            payment_method='CASH'
        )

        Payment.objects.create(
            user=user2,
            paid_lesson=lesson,
            amount=29.99,
            payment_method='TRANSFER'
        )

        self.stdout.write(self.style.SUCCESS('Успешно записаны данные о платежах'))

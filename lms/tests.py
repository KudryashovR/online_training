from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from lms.models import Course, Lesson
from users.models.user_model import CustomUser


class CourseViewSetTest(APITestCase):
    """
    Набор тестов для проверки работы API, связанного с курсами и уроками.
    """

    def setUp(self):
        """
        Настройка тестовой среды, создание пользователей, групп, курса и урока.
        """

        self.client = APIClient()

        self.user = CustomUser.objects.create_user(email='testuser@test.ts', password='password')
        self.moderator = CustomUser.objects.create_user(email='moderator@test.ts', password='password')

        self.moderators_group = Group.objects.create(name='Модераторы')
        self.moderators_group.user_set.add(self.moderator)

        self.course = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)

        self.lesson = Lesson.objects.create(title='Test Lesson', description='Lesson Content', course=self.course,
                                            video_url='http://youtube.com/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9',
                                            owner=self.user)

    def test_create_lesson(self):
        """
        Тест создания нового урока.
        """

        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/lessons/', {
            'title': 'New Lesson',
            'description': 'Content of new lesson',
            'course': self.course.id,
            'video_url': 'http://youtube.com/video.mp4',
            'owner': self.user.id
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_lesson(self):
        """
        Тест получения информации о существующем уроке.
        """

        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/lessons/{self.lesson.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        """
        Тест обновления данных существующего урока.
        """

        self.client.force_authenticate(user=self.user)
        response = self.client.put(f'/api/lessons/{self.lesson.id}/', {
            'title': 'Updated Lesson',
            'description': 'Updated content',
            'course': self.course.id,
            'video_url': 'http://youtube.com/video2.mp4',
            'owner': self.user.id
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        """
        Тест удаления существующего урока.
        """

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/lessons/{self.lesson.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_lessons(self):
        """
        Тест получения списка всех уроков.
        """

        self.client.force_authenticate(user=self.moderator)
        response = self.client.get('/api/lessons/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Тест на подписку на обновления курса
    def test_subscribe_to_course_updates(self):
        """
        Тест подписки на обновления курса.
        """

        self.client.force_authenticate(user=self.user)
        data = {'course_id': self.course.id}
        response = self.client.post('/api/subscribe/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Тест на проверку доступности для модераторов
    def test_access_for_moderators(self):
        """
        Тест проверки доступности курса для модераторов.
        """

        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(f'/api/courses/{self.course.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Тест на отказ в доступе для анонимных пользователей
    def test_access_for_anonymous(self):
        """
        Тест отказа в доступе к курсу для анонимных пользователей.
        """

        response = self.client.get(f'/api/courses/{self.course.id}/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

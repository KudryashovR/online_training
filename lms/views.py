from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer, UserProfileSerializer

User = get_user_model()


class CourseViewSet(viewsets.ModelViewSet):
    """
    Предоставляет стандартные действия `CRUD` для модели Course.

    Атрибуты:
      `queryset` : QuerySet
          Набор данных для обработки (все объекты модели Course).
      `serializer_class` : Serializer
          Класс сериализатора для модели Course (CourseSerializer).
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """
    Предоставляет действия `список` и `создание` для модели Lesson.

    Атрибуты:
      `queryset` : QuerySet
          Набор данных для обработки (все объекты модели Lesson).
      `serializer_class` : Serializer
          Класс сериализатора для модели Lesson (LessonSerializer).
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Предоставляет действия `получение`, `обновление` и `удаление` для модели Lesson.

    Атрибуты:
      `queryset` : QuerySet
          Набор данных для обработки (все объекты модели Lesson).
      `serializer_class` : Serializer
          Класс сериализатора для модели Lesson (LessonSerializer).
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class UserProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Предоставляет действия `получение` и `обновление` для пользовательского профиля.

    Атрибуты:
      `queryset` : QuerySet
          Набор данных для обработки (все объекты модели User).
      `serializer_class` : Serializer
          Класс сериализатора для пользовательского профиля (UserProfileSerializer).
      `permission_classes` : list
          Список классов разрешений для контроля доступа (только аутентифицированные пользователи).
    """

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Переопределяет метод, чтобы получить профиль текущего пользователя.

        Возвращает:
            `User` : профиль текущего аутентифицированного пользователя. 
        """
        
        return self.request.user

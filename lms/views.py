from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    """
    UPDATE
    Предоставляет стандартные действия `CRUD` для модели Course.

    Атрибуты:
      `queryset` : QuerySet
          Набор данных для обработки (все объекты модели Course).
      `serializer_class` : Serializer
          Класс сериализатора для модели Course (CourseSerializer).
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['destroy', 'create']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'retrieve', 'list']:
            self.permission_classes = [IsAuthenticated, IsModerator]
        return [permission() for permission in self.permission_classes]


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """
    UPDATE
    Предоставляет действия `список` и `создание` для модели Lesson.

    Атрибуты:
      `queryset` : QuerySet
          Набор данных для обработки (все объекты модели Lesson).
      `serializer_class` : Serializer
          Класс сериализатора для модели Lesson (LessonSerializer).
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated, IsModerator]
        return [permission() for permission in self.permission_classes]


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    UPDATE
    Предоставляет действия `получение`, `обновление` и `удаление` для модели Lesson.

    Атрибуты:
      `queryset` : QuerySet
          Набор данных для обработки (все объекты модели Lesson).
      `serializer_class` : Serializer
          Класс сериализатора для модели Lesson (LessonSerializer).
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'retrieve']:
            self.permission_classes = [IsAuthenticated, IsModerator]
        return [permission() for permission in self.permission_classes]

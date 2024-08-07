from rest_framework import viewsets, generics

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer


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

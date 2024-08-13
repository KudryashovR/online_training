from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsNotModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """
    UPDATE
    ViewSet для работы с курсами.

    - Создание и удаление курсов доступны только аутентифицированным пользователям.
    - Просмотр и редактирование курсов доступны модераторам (пользователям, состоящим в группе "Moderators").

    Атрибуты:
        queryset: QuerySet с объектами курса.
        serializer_class: Класс сериализатора для курсов.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """
        Возвращает список разрешений, необходимых для текущего действия.

        Возвращаемое значение:
            Список экземпляров разрешений.
        """

        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['destroy', 'update', 'partial_update', 'retrieve', 'list']:
            self.permission_classes = [IsAuthenticated, IsOwner | IsNotModerator]

        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Course.objects.all()

        return Course.objects.filter(owner=self.request.user)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """
    UPDATE
    APIView для списка и создания уроков.

    - Создание уроков доступно только аутентифицированным пользователям.
    - Просмотр списка уроков доступен модераторам (пользователям, состоящим в группе "Moderators").

    Атрибуты:
        queryset: QuerySet с объектами уроков.
        serializer_class: Класс сериализатора для уроков.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        """
        Возвращает список разрешений, необходимых для текущего действия.

        Возвращаемое значение:
            Список экземпляров разрешений.
        """

        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        elif self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated, IsNotModerator]

        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    UPDATE
    APIView для получения, обновления и удаления уроков.

    - Удаление уроков доступно только аутентифицированным пользователям.
    - Получение и обновление уроков доступно модераторам (пользователям, состоящим в группе "Moderators").

    Атрибуты:
        queryset: QuerySet с объектами уроков.
        serializer_class: Класс сериализатора для уроков.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        """
        Возвращает список разрешений, необходимых для текущего действия.

        Возвращаемое значение:
            Список экземпляров разрешений.
        """

        if self.request.method == 'DELETE':
            self.permission_classes = [IsAuthenticated, IsOwner | IsNotModerator]
        elif self.request.method in ['PATCH', 'PUT', 'GET']:
            self.permission_classes = [IsAuthenticated, IsOwner | IsNotModerator]

        return [permission() for permission in self.permission_classes]

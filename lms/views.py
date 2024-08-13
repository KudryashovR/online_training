from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для работы с курсами. Поддерживает все стандартные операции CRUD.

    Атрибуты:
        queryset (QuerySet): Запрос для получения всех объектов Course.
        serializer_class (Serializer): Класс сериализатора для модели Course.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """
        Определяет и возвращает разрешения для текущего действия.

        Возвращаемое значение:
            list: Список экземпляров классов разрешений.
        """

        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['destroy', 'update', 'partial_update', 'retrieve', 'list']:
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]

        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        """
        Переопределяет метод для сохранения владельца курса при создании.

        Аргументы:
            serializer (Serializer): Сериализатор данных.
        """

        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Возвращает queryset для вьюсета в зависимости от пользователя.

        Возвращаемое значение:
            QuerySet: Запрос для получения объектов Course, доступных текущему пользователю.
        """

        if self.request.user.groups.filter(name='Модераторы').exists():
            return Course.objects.all()

        return Course.objects.filter(owner=self.request.user)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """
    API представление для создания и получения списка уроков.

    Атрибуты:
        queryset (QuerySet): Запрос для получения всех объектов Lesson.
        serializer_class (Serializer): Класс сериализатора для модели Lesson.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        """
        Определяет и возвращает разрешения для текущего запроса.

        Возвращаемое значение:
            list: Список экземпляров классов разрешений.
        """

        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        elif self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated, IsModerator]

        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        """
        Переопределяет метод для сохранения владельца урока при создании.

        Аргументы:
            serializer (Serializer): Сериализатор данных.
        """

        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Возвращает queryset для представления в зависимости от пользователя.

        Возвращаемое значение:
            QuerySet: Запрос для получения объектов Lesson, доступных текущему пользователю.
        """

        if self.request.user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API представление для получения, обновления и удаления уроков.

    Атрибуты:
        queryset (QuerySet): Запрос для получения всех объектов Lesson.
        serializer_class (Serializer): Класс сериализатора для модели Lesson.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        """
        Определяет и возвращает разрешения для текущего запроса.

        Возвращаемое значение:
            list: Список экземпляров классов разрешений.
        """

        if self.request.method == 'DELETE':
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.request.method in ['PATCH', 'PUT', 'GET']:
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]

        return [permission() for permission in self.permission_classes]

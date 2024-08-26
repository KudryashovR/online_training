from pprint import pprint

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy
from rest_framework.views import APIView

from lms.models import Course, Lesson, Subscription
from lms.paginators import LessonsAndCoursesPageNumberPagination
from lms.serializers import CourseSerializer, LessonSerializer
from lms.services.stripe_service import create_product, create_price, create_checkout_session
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для работы с курсами. Поддерживает все стандартные операции CRUD.

    Атрибуты:
        queryset (QuerySet): Запрос для получения всех объектов Course.
        serializer_class (Serializer): Класс сериализатора для модели Course.
        pagination_class (Class): Класс пагинации, применяемый к результатам.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = LessonsAndCoursesPageNumberPagination

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
        pagination_class (Class): Класс пагинации, применяемый к результатам.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonsAndCoursesPageNumberPagination

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


class SubscriptionView(APIView):
    """
    Представление для управления подписками на курсы.

    Это представление позволяет аутентифицированным пользователям добавлять или удалять подписки на курсы.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST-запрос для добавления или удаления подписки на курс.

        Если пользователь уже подписан на указанный курс, подписка будет удалена. Если не подписан, подписка будет
        создана.

        Параметры
        ----------
        request : Request
            Объект запроса с данными от клиента.

        *args : list
            Дополнительные позиционные аргументы.

        **kwargs : dict
            Дополнительные именованные аргументы.

        Возвращает
        -------
        Response
            Ответ с сообщением о результате операции.

        Содержимое
        ----------
        message : str
            Сообщение, указывающее, было ли выполнено добавление или удаление подписки.
        """

        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'подписка добавлена'

        return Response({"message": message})


class CreatePaymentAPIView(APIView):

    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)

        if not course.stripe_product_id:
            product = create_product(course.title, course.description)
            course.stripe_product_id = product.id
            course.save()

        if not course.stripe_price_id:
            price = create_price(course.stripe_product_id, course.price)
            course.stripe_price_id = price.id
            course.save()

        success_url = request.build_absolute_uri(reverse('lms:payment-success'))
        cancel_url = request.build_absolute_uri(reverse('lms:payment-cancel'))
        session = create_checkout_session(course.stripe_price_id, success_url, cancel_url)

        if session is None:
            return Response({'error': 'Failed to create checkout session'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'id': session.id, 'url': session.url}, status=status.HTTP_200_OK)


def payment_success(request):
    return JsonResponse(data={"answer": "Payment was successful!"}, status=status.HTTP_200_OK)

def payment_cancel(request):
    return JsonResponse(data={"answer": "Payment was cancelled."}, status=status.HTTP_200_OK)

from django.contrib.auth import get_user_model
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models.payment_model import Payment
from users.models.user_model import CustomUser
from users.serializers import PaymentSerializer, UserProfileSerializer, PublicUserProfileSerializer

User = get_user_model()


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления объектами модели Payment.

    Этот ViewSet предоставляет стандартные действия CRUD для модели Payment, а также возможности фильтрации
    и сортировки данных.

    Атрибуты:
        queryset (QuerySet): База данных, содержащая все объекты модели Payment.
        serializer_class (Serializer): Класс сериализатора, который будет использоваться
                                       для преобразования объектов модели Payment.
        filter_backends (list): Список бекэндов фильтрации, используемых для фильтрации и сор-
                                тировки данных.
        filterset_fields (list): Список полей, по которым возможна фильтрация. В данном случае,
                                 возможна фильтрация по полям 'paid_course', 'paid_lesson' и
                                 'payment_method'.
        ordering_fields (list): Список полей, по которым возможна сортировка. В данном случае,
                                сортировка возможна по полю 'payment_date'.
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']


class UserProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    UPDATE
    Предоставляет действия `получение` и `обновление` для пользовательского профиля.

    Атрибуты:
      `queryset` : QuerySet
          Набор данных для обработки (все объекты модели User).
      `permission_classes` : list
          Список классов разрешений для контроля доступа (только аутентифицированные пользователи).
    """

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Определяет класс сериализатора для разных методов.

        Возвращает:
            class: Класс сериализатора, соответствующий текущему методу запроса.
        """
        if self.request.method in ['PUT', 'PATCH']:
            return UserProfileSerializer
        return PublicUserProfileSerializer

    def get_object(self):
        """
        Переопределяет метод для получения профиля текущего пользователя при выполнении действий обновления или удаления,
        и получения указанного пользователя при выполнении действия получения.

        Возвращает:
            User: Профиль текущего аутентифицированного пользователя.
        """
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return self.request.user
        return super().get_object()

class UserCreate(generics.CreateAPIView):
    """
    Класс представления для создания нового пользователя.

    Атрибуты:
        queryset (QuerySet): Набор запросов для модели CustomUser.
        serializer_class (Serializer): Класс сериализатора, используемый для валидации и десериализации входных данных.
        permission_classes (list): Список классов разрешений, применяемых к этому представлению. В данном случае
                                   разрешен доступ для всех.
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

class UserList(generics.ListAPIView):
    """
    Класс представления для получения списка пользователей.

    Атрибуты:
        queryset (QuerySet): Набор запросов для модели CustomUser.
        serializer_class (Serializer): Класс сериализатора, используемый для сериализации данных.
        permission_classes (list): Список классов разрешений, применяемых к этому представлению. В данном случае доступ
                                   разрешен только для аутентифицированных пользователей.
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

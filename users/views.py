from django.contrib.auth import get_user_model
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from users.models import Payment
from users.serializers import PaymentSerializer, UserProfileSerializer

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

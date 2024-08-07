from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from users.models import Payment
from users.serializers import PaymentSerializer


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

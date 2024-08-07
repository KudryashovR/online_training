from django_filters import rest_framework as filters

from users.models import Payment


class PaymentFilter(filters.FilterSet):
    course = filters.CharFilter(field_name="course__name", lookup_expr='icontains')
    lesson = filters.CharFilter(field_name="lesson__name", lookup_expr='icontains')
    payment_method = filters.CharFilter(field_name="payment_method", lookup_expr='icontains')

    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'payment_method']

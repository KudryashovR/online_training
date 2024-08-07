from rest_framework import serializers

from users.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Payment.

    Этот сериализатор преобразует объекты модели Payment в формат JSON и обратно для использования в API.

    Класс Meta:
        model : Model
            Модель, используемая для сериализации (Payment).
        fields : str
            Поля модели, которые будут включены в сериализацию ('__all__' означает, что все поля будут включены).
    """

    class Meta:
        model = Payment
        fields = '__all__'

from rest_framework import serializers

from users.models import Payment, CustomUser


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


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор профиля пользователя. Этот класс предназначен для преобразования данных профиля пользователя в формат
    JSON и обратно.

    Атрибуты
    --------
    payment_history : PaymentSerializer
        Сериализатор для вывода истории платежей пользователя. Использует сериализатор PaymentSerializer
        для отображения связанных платежей. Поле many=True указывает, что может быть несколько платежей, read_only=True
        делает это поле только для чтения, а source='payments' указывает на имя обратного отношения в модели платежей.

    Метакласс
    ---------
    Meta
        model : CustomUser
            Указывает модель, с которой работает данный сериализатор.
        fields : str
            Поле 'all' указывает, что необходимо сериализовать все поля модели CustomUser.
    """

    payment_history = PaymentSerializer(many=True, read_only=True, source='payments')

    class Meta:
        model = CustomUser
        fields = '__all__'

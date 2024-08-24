from rest_framework import serializers

from users.models.user_model import CustomUser
from users.models.payment_model import Payment


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


class PublicUserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для публичного отображения профиля пользователя.
    """

    class Meta:
        model = CustomUser
        fields = ['email', 'city', 'avatar']

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для профиля пользователя.
    """

    payment_history = PaymentSerializer(many=True, read_only=True, source='payments')

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'phone', 'city', 'avatar', 'payment_history']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data['phone'],
            city=validated_data['city']
        )

        return user

from django.contrib.auth import get_user_model
from rest_framework import serializers

from lms.models import Course, Lesson

User = get_user_model()


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Course.

    Класс Meta:
        model : Model
            Модель, используемая для сериализации (Course).
        fields : str
            Поля модели, которые будут включены в сериализацию ('all' означает, что все поля будут включены).
    """

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Lesson.

    Класс Meta:
        model : Model
            Модель, используемая для сериализации (Lesson).
        fields : str
            Поля модели, которые будут включены в сериализацию ('all' означает, что все поля будут включены).
    """

    class Meta:
        model = Lesson
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользовательского профиля (модель User).

    Класс Meta:
        model : Model
            Модель, используемая для сериализации (User).
        fields : list
            Поля модели, которые будут включены в сериализацию (['id', 'email', 'phone', 'city', 'avatar']).
    """

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar']

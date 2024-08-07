from django.contrib.auth import get_user_model
from rest_framework import serializers

from lms.models import Course, Lesson

User = get_user_model()


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Course.

    Атрибуты
    ----------
    lesson_count : SerializerMethodField
        Поле для подсчета числа уроков в курсе. Определено как динамическое поле.

    Класс Meta:
        Атрибуты
        ----------
        model : Model
            Модель, используемая для сериализации (Course).
        fields : list[str]
            Поля модели, которые будут включены в сериализацию ('all' означает, что все поля будут включены).
    """

    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    @staticmethod
    def get_lesson_count(instance):
        """
        Возвращает количество уроков для данного курса.

        Параметры
        ----------
        instance : Course
            Экземпляр курса, для которого вычисляется количество уроков.

        Возвращает
        -------
        int
            Количество уроков для данного курса.
        """

        return Lesson.objects.filter(course=instance).count()


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

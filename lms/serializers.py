from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from lms.models import Course, Lesson, Subscription
from lms.validators import LinkValidator

from lms.tasks import send_update_email

User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Lesson.

    Класс Meta:
        model : Model
            Модель, используемая для сериализации (Lesson).
        fields : str
            Поля модели, которые будут включены в сериализацию ('all' означает, что все поля будут включены).
        validators : list
            Список валидаторов, которые будут применяться к сериализованным данным. В данном случае используется
            LinkValidator для проверки поля 'video_url'.
    """

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(field='video_url')]

    def update(self, instance, validated_data):
        """
        Обновляет экземпляр Lesson с использованием данных validated_data.

        При обновлении также проверяется, обновлялся ли связанный курс более 4 часов назад.
        Если да, то подписчики курса получают уведомление по электронной почте об обновлении урока.

        Параметры:
        instance : Lesson
            Экземпляр урока, который нужно обновить.
        validated_data : dict
            Данные, прошедшие валидацию и использующиеся для обновления урока.

        Возврат:
        Lesson : Обновленный экземпляр урока.
        """

        now = timezone.now()
        four_hours_ago = now - timedelta(hours=4)
        updated_course = Course.objects.filter(pk=instance.course_id, updated_at__lte=four_hours_ago).last()

        if updated_course:
            subscribers = Subscription.objects.filter(course=updated_course)
            subscribed_users = [subscription.user for subscription in subscribers]

            for user in subscribed_users:
                send_update_email.delay(user.email, instance.title)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Course.

    Атрибуты
    ----------
    lessons : LessonSerializer
        Поле для отображения подробной информации обо всех уроках курса.
    lesson_count : SerializerMethodField
        Поле для подсчета числа уроков в курсе. Определено как динамическое поле.
    is_subscribed : SerializerMethodField
        Поле, отображающее статус подписки текущего пользователя на данный курс.

    Класс Meta
    ----------
    model : Model
        Модель, используемая для сериализации (Course).
    fields : list[str] или str
        Поля модели, которые будут включены в сериализацию.
        При значении 'all' включаются все поля модели.

    Методы
    -------
    get_is_subscribed(obj):
        Определяет, подписан ли текущий пользователь на данный курс.

        Параметры
        ----------
        obj : Course
            Текущий сериализуемый объект курса.

        Возвращает
        -------
        bool
            True, если пользователь подписан на курс, иначе False.

    get_lesson_count(instance):
        Возвращает количество уроков для данного курса.

        Параметры
        ----------
        instance : Course
            Экземпляр курса, для которого вычисляется количество уроков.

        Возвращает
        -------
        int
            Количество уроков для данного курса.

    update(instance, validated_data):
        Обновляет экземпляр курса с использованием данных validated_data.

        При обновлении также уведомляет всех подписчиков курса по электронной почте о произошедших изменениях.

        Параметры
        ----------
        instance : Course
            Экземпляр курса, который нужно обновить.
        validated_data : dict
            Данные, прошедшие валидацию и используемые для обновления курса.

        Возвращает
        -------
        Course
            Обновленный экземпляр курса.
    """

    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_is_subscribed(self, obj):
        """
        Определяет, подписан ли текущий пользователь на данный курс.

        Параметры
        ----------
        obj : Course
            Текущий сериализуемый объект курса.

        Возвращает
        -------
        bool
            True, если пользователь подписан на курс, иначе False.
        """

        user = self.context['request'].user

        return Subscription.objects.filter(user=user, course=obj).exists()

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

        return instance.lessons.count()

    def update(self, instance, validated_data):
        """
        Обновляет экземпляр курса с использованием данных validated_data.

        При обновлении также уведомляет всех подписчиков курса по электронной почте о произошедших изменениях.

        Параметры
        ----------
        instance : Course
            Экземпляр курса, который нужно обновить.
        validated_data : dict
            Данные, прошедшие валидацию и используемые для обновления курса.

        Возвращает
        -------
        Course
            Обновленный экземпляр курса.
        """

        subscribers = Subscription.objects.filter(course=instance)
        subscribed_users = [subscription.user for subscription in subscribers]

        for user in subscribed_users:
            send_update_email.delay(user.email, instance.title)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance

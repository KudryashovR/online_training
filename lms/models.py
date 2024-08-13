from django.db import models

from users.models.user_model import CustomUser


class Course(models.Model):
    """
    Модель Курса.

    Атрибуты:
        title (CharField): Наименование курса.
        preview (ImageField): Изображение для курса (может быть пустым).
        description (TextField): Описание курса.
        owner (ForeignKey): Владелец курса, ссылка на пользователя.

    Методы:
        __str__: Возвращает строковое представление курса.
    """

    title = models.CharField(max_length=200, verbose_name='наименование')
    preview = models.ImageField(upload_to='course_previews/', blank=True, null=True, verbose_name='изображение')
    description = models.TextField(verbose_name='описание')
    owner = models.ForeignKey(CustomUser, related_name='courses', on_delete=models.CASCADE)

    def __str__(self):
        """
        Возвращает строковое представление курса.

        Возвращаемое значение:
            str: Название курса.
        """

        return self.title

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    """
    Модель Урока.

    Атрибуты:
        course (ForeignKey): Курс, к которому относится урок.
        title (CharField): Название урока.
        description (TextField): Описание урока.
        preview (ImageField): Изображение для урока (может быть пустым).
        video_url (URLField): URL-адрес видео.
        owner (ForeignKey): Владелец урока, ссылка на пользователя.

    Методы:
        __str__: Возвращает строковое представление урока.
    """

    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='lesson_previews/', blank=True, null=True, verbose_name='изображение')
    video_url = models.URLField(verbose_name='видео')
    owner = models.ForeignKey(CustomUser, related_name='lessons', on_delete=models.CASCADE)

    def __str__(self):
        """
        Возвращает строковое представление урока.

        Возвращаемое значение:
            str: Название урока.
        """

        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

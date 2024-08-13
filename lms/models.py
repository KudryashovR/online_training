from django.db import models

from users.models.user_model import CustomUser


class Course(models.Model):
    """
    UPDATE
    Класс Course представляет курс.

    Атрибуты:
    ----------
    title : str
        Наименование курса (максимальная длина 200 символов).
    preview : ImageField
        Изображение для предварительного просмотра курса (необязательное поле, загружается в 'course_previews/').
    description : str
        Описание курса.
    """

    title = models.CharField(max_length=200, verbose_name='наименование')
    preview = models.ImageField(upload_to='course_previews/', blank=True, null=True, verbose_name='изображение')
    description = models.TextField(verbose_name='описание')
    owner = models.ForeignKey(CustomUser, related_name='courses', on_delete=models.CASCADE)

    def __str__(self):
        """
        Возвращает строковое представление курса - его наименование.
        """

        return self.title

    class Meta:
        """
        Метаданные для класса Course.

        verbose_name : str
            Человекочитаемое имя модели в единственном числе.
        verbose_name_plural : str
            Человекочитаемое имя модели во множественном числе.
        """

        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    """
    UPDATE
    Класс Lesson представляет урок, который является частью курса.

    Атрибуты:
    ----------
    course : ForeignKey
        Ссылка на курс, к которому относится данный урок. При удалении курса, уроки также удаляются.
    title : str
        Наименование урока (максимальная длина 200 символов).
    description : str
        Описание урока.
    preview : ImageField
        Изображение для предварительного просмотра урока (необязательное поле, загружается в 'lesson_previews/').
    video_url : URLField
        URL на видео урока.
    """

    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='lesson_previews/', blank=True, null=True, verbose_name='изображение')
    video_url = models.URLField(verbose_name='видео')
    owner = models.ForeignKey(CustomUser, related_name='lessons', on_delete=models.CASCADE)

    def __str__(self):
        """
        Возвращает строковое представление урока - его наименование.
        """

        return self.title

    class Meta:
        """
        Метаданные для класса Lesson.

        verbose_name : str
            Человекочитаемое имя модели в единственном числе.
        verbose_name_plural : str
            Человекочитаемое имя модели во множественном числе.
        """

        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

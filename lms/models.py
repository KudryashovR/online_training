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
        price (IntegerField): Цена курса.
        stripe_product_id (CharField): Идентификатор продукта в Stripe (может быть пустым).
        stripe_price_id (CharField): Идентификатор цены в Stripe (может быть пустым).

    Методы:
        str: Возвращает строковое представление курса.
    """

    title = models.CharField(max_length=200, verbose_name='наименование')
    preview = models.ImageField(upload_to='course_previews/', blank=True, null=True, verbose_name='изображение')
    description = models.TextField(verbose_name='описание')
    owner = models.ForeignKey(CustomUser, related_name='courses', on_delete=models.CASCADE)
    price = models.IntegerField(help_text="цена")
    stripe_product_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='время изменения')

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


class Subscription(models.Model):
    """
    Модель Subscription представляет собой подписку пользователя на курс.

    Атрибуты:
    ----------
    user : ForeignKey
        Ссылка на модель CustomUser, представляющая пользователя, сделавшего подписку. При удалении пользователя
        все его подписки также удаляются (on_delete=models.CASCADE).

    course : ForeignKey
        Ссылка на модель Course, представляющая курс, на который пользователь подписан. При удалении курса все связанные
         подписки также удаляются (on_delete=models.CASCADE).

    Методы:
    -------
    __str__():
        Возвращает строковое представление объекта подписки в формате "пользователь подписан на курс".
    """

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="courses")

    def __str__(self):
        return f"{self.user} подписан на {self.course}"

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'

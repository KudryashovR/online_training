from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name='наименование')
    preview = models.ImageField(upload_to='course_previews/', blank=True, null=True, verbose_name='изображение')
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='lesson_previews/', blank=True, null=True, verbose_name='изображение')
    video_url = models.URLField(verbose_name='видео')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

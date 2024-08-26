from django.core.exceptions import ValidationError
from django.db import models

from lms.models import Course, Lesson
from users.models.user_model import CustomUser


class Payment(models.Model):
    """
    Модель Payment (Платеж).

    Поля:
    -----
    user : ForeignKey
        Ссылка на модель пользователя (CustomUser), который произвел платеж.
    payment_date : DateTimeField
        Дата и время осуществления платежа.
    paid_course : ForeignKey, optional
        Ссылка на оплаченный курс. Может быть пустым.
    paid_lesson : ForeignKey, optional
        Ссылка на оплаченный урок. Может быть пустым.
    amount : DecimalField
        Сумма оплаты.
    payment_method : CharField
        Способ оплаты, возможные значения - 'CASH' (наличные) и 'TRANSFER' (перевод на счет).
    stripe_payment_id : CharField
        Идентификатор транзакции в Stripe. Может быть пустым.
    stripe_status : CharField
        Статус транзакции в Stripe. Может быть пустым.

    Методы:
    -------
    __str__():
        Возвращает строковое представление платежа.

    Классы Meta:
    ------------
    verbose_name : str
        Человекочитаемое название модели в единственном числе.
    verbose_name_plural : str
        Человекочитаемое название модели во множественном числе.
    """

    PAYMENT_METHOD_CHOICES = [
        ('CASH', 'Наличные'),
        ('TRANSFER', 'Перевод на счет'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="payments")
    payment_date = models.DateTimeField(auto_now_add=True)
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name="payments")
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    stripe_payment_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="id транзакции")
    stripe_status = models.CharField(max_length=20, null=True, verbose_name="статус транзакции")

    def __str__(self):
        return f"Платеж от {self.user.email} на сумму {self.amount}"

    def clean(self):
        """
        Проверяет правильность заполнения полей перед сохранением записи в базу данных.

        Проверяет, что поля stripe_payment_id и stripe_status заполнены, если payment_method равен 'TRANSFER'.
        Если поле не заполнено и его заполнение обязательно, возбуждает ValidationError.
        """

        if self.payment_method == 'TRANSFER' and not self.stripe_payment_id and not self.stripe_status:
            raise ValidationError("Поля 'stripe_payment_id' и 'stripe_status' должны быть заполнены, если метод оплаты "
                                  "'TRANSFER'.")

    def save(self, *args, **kwargs):
        """
        Сохраняет запись в базу данных.

        Перед сохранением проверяет запись с помощью clean().
        """

        self.clean()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'

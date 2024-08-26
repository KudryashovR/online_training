from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models.payment_model import Payment
from users.models.user_model import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Настраивает интерфейс администратора Django для модели CustomUser.

    Атрибуты:
        model : Model
            Ссылка на модель CustomUser.
        list_display : tuple
            Список полей, отображаемых в изменяемом списке объектов.
        list_filter : tuple
            Список полей, по которым производится фильтрация в изменяемом списке объектов.
        fieldsets : tuple
            Определяет разделы и поля, отображаемые при просмотре/изменении объекта.
        add_fieldsets : tuple
            Определяет разделы и поля, отображаемые при добавлении нового объекта.
        search_fields : tuple
            Список полей, по которым будет производиться поиск.
        ordering : tuple
            Определяет порядок сортировки объектов в списке.
    """

    model = CustomUser
    list_display = ('email', 'phone', 'city', 'is_staff', 'is_active',)
    list_filter = ('email', 'phone', 'city', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'phone', 'city', 'avatar')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Groups', {'fields': ('groups',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Payment)

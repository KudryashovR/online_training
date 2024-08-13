from rest_framework.permissions import BasePermission


class IsNotModerator(BasePermission):
    """
    Разрешение, предоставляющее доступ только модераторам.

    Пользователь должен состоять в группе 'Модераторы', чтобы иметь это разрешение.

    Методы:
        has_permission(request, view): Проверяет, что пользователь находится в группе 'Модераторы'.
    """

    def has_permission(self, request, view):
        """
        Проверяет, что пользователь имеет разрешение для доступа к представлению.

        Аргументы:
            request: Объект запроса DRF.
            view: Представление, для которого определяется разрешение.

        Возвращаемое значение:
            bool: True, если пользователь состоит в группе 'Модераторы', иначе False.
        """

        return request.user.groups.filter(name='Модераторы').exists()


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

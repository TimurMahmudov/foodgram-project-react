from rest_framework import permissions


class AccessUpdateAndDelete(permissions.BasePermission):
    """
    Разрешение на редактирование/удаление рецептов
    """
    def has_object_permission(self, request, view, obj):
        return (request.user == obj.author
                or request.method in permissions.SAFE_METHODS)

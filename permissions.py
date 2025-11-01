from rest_framework import permissions
from .models import Advertisement

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение на изменение/удаление только для владельца объявления.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешаем чтение для всех запросов
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Разрешаем запись только владельцу
        return obj.creator == request.user

class IsOwner(permissions.BasePermission):
    """
    Разрешение только для владельца объявления.
    """
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user
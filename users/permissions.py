from rest_framework.permissions import BasePermission


class Staff(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name="Модераторы").exists():
            return True

        return False


class Is_Users(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name="Пользователи").exists():
            return True

        return False


class Owner(BasePermission):
    def has_permission(self, request, view):
        if request.user.owner:
            return True

        return False

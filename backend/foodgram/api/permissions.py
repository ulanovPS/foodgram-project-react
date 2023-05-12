from rest_framework import permissions


class GuestIsReadOnlyAdminOrOwnerFullAccess(permissions.BasePermission):
    """
    GUEST - только просмотр.
    ADMIN - или OWNER все методы.
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.user_id == request.user
                or request.user.is_superuser)


class GuestIsReadOnlyAdminOrUserFullAccess(permissions.BasePermission):
    """
    GUEST - только просмотр.
    ADMIN или USER - возможны остальные методы.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.id == request.user
                or request.user.is_superuser)

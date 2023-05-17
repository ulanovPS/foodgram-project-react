from rest_framework import permissions


class GuestIsReadOnlyAdminOrOwnerFullAccess(permissions.BasePermission):
    """ GUEST - только просмотр, ADMIN - или OWNER все методы """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.author == request.user
                or request.user.is_superuser)

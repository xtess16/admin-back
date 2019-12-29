from rest_framework import permissions


class AuthGroupPermission(permissions.BasePermission):
    """
    AuthGroupPermission
    """

    def has_permission(self, request, view):
        for g in request.user.groups.all():
            print(1, g.id)
        return True

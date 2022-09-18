from rest_framework import permissions


class UserSignupPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsAdminOrSuperUser(permissions.BasePermission):
    """Admin or Super User permission."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )


class IsOwnerOrModeratorOrAdmin(permissions.BasePermission):
    """Owner or Moderator or Admin permission."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
            or request.user.is_superuser
        )

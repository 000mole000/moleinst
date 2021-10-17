from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCurrentUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user
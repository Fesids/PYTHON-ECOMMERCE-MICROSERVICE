from rest_framework.permissions import BasePermission

class IsExternal(BasePermission):
    def has_permission(self, request, view):
       return bool(request.user.is_external and request.user.is_authenticated)
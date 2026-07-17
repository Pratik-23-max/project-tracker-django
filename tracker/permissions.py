from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsManagerOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        # Everyone who is logged in can view data
        if request.method in SAFE_METHODS:
            return True

        # Only manager (superuser) can create/update/delete
        return request.user.is_superuser
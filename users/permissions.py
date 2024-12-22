from rest_framework.permissions import BasePermission

class IsOwnerOrPostOnly(BasePermission):
    """
    Allows:
    - Only administrators to access the list method.
    - Any user to create new records (POST).
    - Only the owner of the object (or administrators) to access, modify, or delete specific records.
    """

    def has_permission(self, request, view):
        if view.action == 'create':
            return True

        if view.action == 'list':
            return request.user and request.user.is_staff

        return True

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return obj == request.user or request.user.is_staff

        return False

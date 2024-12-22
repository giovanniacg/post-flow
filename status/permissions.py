from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    """
    Allows:
    - Only administrators can POST, PUT, PATCH, or DELETE.
    - Only Authenticated users can GET.
    """

    def has_permission(self, request, view):
        if request.method in ['GET'] or view.action == 'list':
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET']:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff

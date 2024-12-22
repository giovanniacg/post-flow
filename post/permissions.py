from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    """
    Allows:
    - Only the owner of the object or admin can GET
    - Only the authenticated can POST
    - Only admin can PUT, PATCH, or DELETE
    """

    def has_permission(self, request, view):
        if request.method in ['POST', 'GET']:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in ['POST', 'GET']:
            return obj.user == request.user or request.user.is_staff
        return request.user and request.user.is_staff
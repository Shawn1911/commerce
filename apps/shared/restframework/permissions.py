from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner') and obj.owner != request.user:
            raise PermissionDenied('You do not have permission for this shop!')

        if hasattr(obj, 'shop') or hasattr(obj, 'category') and not hasattr(obj, 'owner'):
            if request.method == 'GET' or request.user.default_shop_id == view.kwargs['shop_id']:
                return super().has_object_permission(request, view, obj)
            raise PermissionDenied('You do not have permission to perform this action.')
        return super().has_object_permission(request, view, obj)

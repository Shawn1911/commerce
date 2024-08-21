# permissions.py

from rest_framework.permissions import BasePermission


class IsOwnerOfShop(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


# permissions.py

class IsOwnerOfShopCategory(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.shop.owner == request.user

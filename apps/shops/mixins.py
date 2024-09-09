from rest_framework.generics import get_object_or_404
from shops.models import Shop


class ShopMixin:
    def get_shop(self):
        if self.request.user.is_anonymous:
            return
        return get_object_or_404(Shop, pk=self.kwargs.get("shop_id"))

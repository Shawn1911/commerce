from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from shared import IsOwner
from shops.filters import CustomSearchFilter
from shops.mixins import ShopMixin
from shops.models import Category
from shops.paginations import CustomPagination
from shops.serializers.categories import CategoryDynamicFieldsModelSerializer


@extend_schema(tags=['categories'])
class CategoryModelViewSet(ModelViewSet, ShopMixin):
    queryset = Category.objects.all()
    serializer_class = CategoryDynamicFieldsModelSerializer
    pagination_class = CustomPagination
    filter_backends = OrderingFilter, CustomSearchFilter
    permission_classes = IsAuthenticated, IsOwner
    search_fields = ('name',)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['shop'] = self.get_shop()
        return context

    def get_queryset(self):
        shop = self.get_shop()
        if self.action == 'list':
            if shop.owner != self.request.user:
                raise PermissionDenied({'detail': 'You do not have permission to perform this action.'})
            return super().get_queryset().filter(shop=shop)

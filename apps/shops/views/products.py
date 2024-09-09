from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from shared import IsOwner
from shops.filters import CustomSearchFilter
from shops.mixins import ShopMixin
from shops.models import Product
from shops.paginations import CustomPagination
from shops.serializers.products import ProductDynamicFieldsModelSerializer


@extend_schema(tags=['products'])
@extend_schema_view(
    list=extend_schema(
        responses=ProductDynamicFieldsModelSerializer(ref_name='product_list')),
    create=extend_schema(responses=ProductDynamicFieldsModelSerializer(
        ref_name='product_create',
        fields=['name', 'description', 'category', 'full_price', 'price', 'stock_status', 'unit'])),
    update=extend_schema(responses=ProductDynamicFieldsModelSerializer(
        ref_name='product_update',
        fields=['category']))
)
class ProductModelViewSet(ModelViewSet, ShopMixin):
    queryset = Product.objects.all()
    serializer_class = ProductDynamicFieldsModelSerializer
    filter_backends = CustomSearchFilter, OrderingFilter
    pagination_class = CustomPagination
    permission_classes = IsAuthenticated, IsOwner
    search_fields = ('name',)
    ordering_fields = ('id', 'name', 'price', 'category__name', 'position')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['shop'] = self.get_shop()
        return context

    def get_queryset(self):
        if self.action == 'list':
            if self.get_shop().owner != self.request.user:
                raise PermissionDenied('You do not have permission to perform this action.')
        return super().get_queryset().filter(category__shop=self.get_shop())

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        if self.action == 'list':
            return self.serializer_class(ref_name='product_list', *args, **kwargs)
        elif self.action == 'create':
            return self.serializer_class(
                ref_name='product_create',
                *args, **kwargs,
                fields=['name', 'description', 'category', 'full_price', 'price', 'stock_status', 'unit'])
        return self.serializer_class(*args, ref_name='product_update', **kwargs, exclude=['category'])

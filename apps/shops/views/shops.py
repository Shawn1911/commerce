from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (ListAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,)
from rest_framework.permissions import AllowAny, IsAuthenticated
from shared import IsOwner
from shops.models import Country, Currency, Language, Shop, ShopCategory
from shops.paginations import CustomPagination
from shops.serializers import (CountryModelSerializer, CurrencyModelSerializer,
                               LanguageDynamicFieldsModelSerializer,
                               ShopCategoryModelSerializer,
                               ShopDynamicFieldsModelSerializer,
                               ShopUpdateModelSerializer,)


class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencyModelSerializer
    permission_classes = [IsAuthenticated]


class LanguageListAPIView(ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageDynamicFieldsModelSerializer
    permission_classes = AllowAny,


class CountryListAPIView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryModelSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ('id', 'name', 'code')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['sort_fields'] = self.ordering_fields  # Add sort_fields to the response
        return response


class ShopCategoryListAPIView(ListAPIView):
    queryset = ShopCategory.objects.all()
    serializer_class = ShopCategoryModelSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['shops'])
@extend_schema_view(
    list=extend_schema(responses=ShopDynamicFieldsModelSerializer(ref_name='list', exclude=['owner'])),
    create=extend_schema(responses=ShopDynamicFieldsModelSerializer(
        ref_name='create', fields=['name', 'country', 'phone', 'category', 'currency', 'owner'])))
class ShopListCreateAPIView(ListCreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopDynamicFieldsModelSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        if self.request.method == 'GET':
            return self.serializer_class(ref_name='list', *args, **kwargs, exclude=['owner'])
        return self.serializer_class(
            ref_name='create', *args, **kwargs,
            fields=['name', 'country', 'phone', 'category', 'currency', 'owner'])

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


@extend_schema(tags=['shops'])
class ShopRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Shop.objects.all()
    permission_classes = IsAuthenticated, IsOwner
    serializer_class = ShopUpdateModelSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        if self.request.method == 'GET':
            return ShopDynamicFieldsModelSerializer(*args, **kwargs, exclude=['owner'])
        return self.serializer_class(*args, **kwargs)

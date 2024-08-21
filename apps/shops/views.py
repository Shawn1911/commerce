from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,)
from rest_framework.permissions import IsAuthenticated
from shops.models import Category, Shop
from shops.permissions import IsOwnerOfShop, IsOwnerOfShopCategory
from shops.serializers import (CategoryDetailModelSerializer,
                               CategoryModelSerializer,
                               ShopDetailModelSerializer, ShopModelSerializer,)


@extend_schema(tags=['Shop'])
class ShopListCreateAPIView(ListCreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopModelSerializer
    permission_classes = [IsAuthenticated, IsOwnerOfShop]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = []

    # def get_queryset(self):
    #     if getattr(self, "swagger_fake_view", False):
    #         return Shop.objects.none()
    #     return Shop.objects.filter(owner=self.request.user)
    #
    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


@extend_schema(tags=['Category'])
class CategoryListCreateAPIView(ListCreateAPIView):
    serializer_class = CategoryModelSerializer
    permission_classes = [IsAuthenticated, IsOwnerOfShopCategory]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = []

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Category.objects.none()
        return Category.objects.filter(shop__owner=self.request.user)

    def perform_create(self, serializer):
        shop_id = self.request.data.get('shop')
        shop = Shop.objects.filter(id=shop_id, owner=self.request.user).first()
        if shop:
            serializer.save(shop=shop)
        else:
            raise ValidationError("Invalid shop ID or unauthorized access.")


@extend_schema(tags=['Shop'])
class ShopRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopDetailModelSerializer
    permission_classes = [IsAuthenticated, IsOwnerOfShop]

    def get_queryset(self):
        return Shop.objects.filter(owner=self.request.user)


@extend_schema(tags=['Category'])
class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailModelSerializer
    permission_classes = [IsAuthenticated, IsOwnerOfShopCategory]

    def get_queryset(self):
        return Category.objects.filter(shop__owner=self.request.user)

from django.urls import path
from shops.views import (CategoryListCreateAPIView,
                         CategoryRetrieveUpdateDestroyAPIView,
                         ShopListCreateAPIView,
                         ShopRetrieveUpdateDestroyAPIView,)


urlpatterns = [
    path('shop/', ShopListCreateAPIView.as_view(), name='shop-list-create'),
    path('shop/<int:pk>/detail', ShopRetrieveUpdateDestroyAPIView.as_view(), name='shop-detail'),
    path('shop/<int:pk>/category', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('shop/<int:shop_pk>/category/<int:category_pk>', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail'),
]

from django.urls import include, path
from rest_framework.routers import SimpleRouter
from shops.views import (CountryListAPIView, CurrencyListAPIView,
                         LanguageListAPIView, ShopCategoryListAPIView,
                         ShopListCreateAPIView,
                         ShopRetrieveUpdateDestroyAPIView,)
from shops.views.categories import CategoryModelViewSet
from shops.views.products import ProductModelViewSet


app_name = 'shops'
router = SimpleRouter(False)

router.register('products', ProductModelViewSet, basename='products')
router.register('categories', CategoryModelViewSet, basename='categories')

urlpatterns = [
    path('shop/<int:shop_id>/', include(router.urls)),
    path('currency', CurrencyListAPIView.as_view(), name='currency'),
    path('country', CountryListAPIView.as_view(), name='country'),
    path('shop-category', ShopCategoryListAPIView.as_view(), name='shop_category'),
    path('shop-config', LanguageListAPIView.as_view()),

    path('shop', ShopListCreateAPIView.as_view(), name='shop_list'),
    path('shop/<int:pk>/detail', ShopRetrieveUpdateDestroyAPIView.as_view(), name='shop-detail'),
]

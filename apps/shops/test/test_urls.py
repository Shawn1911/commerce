from django.test import SimpleTestCase
from django.urls import reverse_lazy


class TestShopsUrls(SimpleTestCase):
    def test_shop_urls(self):
        shop_list_create_url = reverse_lazy('shop-list-create')
        assert shop_list_create_url == '/api/v1/shop/shop/'

        shop_detail_url = reverse_lazy('shop-detail', kwargs={'pk': 1})
        assert shop_detail_url == '/api/v1/shop/shop/1/detail'

        category_list_create_url = reverse_lazy('category-list-create', kwargs={'pk': 1})
        assert category_list_create_url == '/api/v1/shop/shop/1/category'

        category_detail_url = reverse_lazy('category-detail', kwargs={'shop_pk': 1, 'category_pk': 1})
        assert category_detail_url == '/api/v1/shop/shop/1/category/1'

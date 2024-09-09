import pytest
from rest_framework.reverse import reverse_lazy


class TestUrl:
    @pytest.mark.parametrize("url,name", [
        ('/api/v1/shop/shop-category', 'shops:shop_category'),
        ('/api/v1/shop/currency', 'shops:currency'),
        ('/api/v1/shop/country', 'shops:country')
    ])
    def test_shop_category_list(self, url, name):
        assert url == reverse_lazy(name)

import pytest
from rest_framework.test import APIClient

from shops.models import (Category, Country, Currency, Product, Shop,
                          ShopCategory, )
from shops.tests.factories import CategoryFactory
from users.models import Plan, User


@pytest.fixture(scope='function')
def api_client():
    yield APIClient()


@pytest.fixture(scope='function')
def user1():
    data = {
        'email': 'tohir@gmail.com',
        'password': '1',
        'is_active': True,
        'is_superuser': False,
        'is_staff': True,
        'type': 'email'
    }

    return User.objects.create_user(**data)


@pytest.fixture(scope='function')
def user2():
    data = {
        'email': 'asqar@gmail.com',
        'password': '1',
        'is_active': True,
        'is_superuser': False,
        'is_staff': True,
        'type': 'email'
    }
    return User.objects.create_user(**data)


@pytest.fixture(scope='function')
def api_user1_client(user1):
    api_client = APIClient()
    api_client.force_authenticate(user1)
    return api_client


@pytest.fixture(scope='function')
def api_user2_client(user2):
    api_client = APIClient()
    api_client.force_authenticate(user2)
    return api_client


@pytest.fixture(scope='function')
def country():
    return Country.objects.create(name='Uzbekistan', code='Uzb')


@pytest.fixture(scope='function')
def shop_category():
    return ShopCategory.objects.create(name='Texnika')


@pytest.fixture(scope='function')
def currency():
    return Currency.objects.create(name="so'm", order=1)


@pytest.fixture(scope='function')
def plan():
    return Plan.objects.create(name="Free", code='free', description='Tekin')


@pytest.fixture(scope='function')
def get_user1():
    return User.objects.first()


@pytest.fixture(scope='function')
def get_country():
    return Country.objects.first()


@pytest.fixture(scope='function')
def get_shop_category():
    return ShopCategory.objects.first()


@pytest.fixture(scope='function')
def get_currency():
    return Currency.objects.first()


@pytest.fixture(scope='function')
def get_plan():
    return Plan.objects.first()


@pytest.fixture(scope='function')
def shop11(user1, country, shop_category, currency, plan):
    shop = Shop.objects.create(
        name="Shop test",
        phone="+998997711310",
        phone_number="998901001010",
        status="active",
        lat=7878700.12,
        lon=7878700.12,
        starts_at=None,
        ends_at=None,
        has_terminal=True,
        about_us="Biz haqimizda malumot",
        facebook="https://facebook.com",
        instagram="https://instagram.com",
        telegram="https://telegram.com",
        email="tohir@gmail.com",
        address="Toshkent",
        is_new_products_show=True,
        is_popular_products_show=True,
        country=country,
        category=shop_category,
        currency=currency,
        owner=user1,
        plan=plan,
    )
    user1.default_shop = shop
    return shop


@pytest.fixture(scope='function')
def shop12(user1, country, shop_category, currency, plan):
    return Shop.objects.create(
        name="Shop test",
        phone="+998997711310",
        phone_number=None,
        status="active",
        lat=7878700.12,
        lon=7878700.12,
        starts_at=None,
        ends_at=None,
        has_terminal=True,
        about_us="Biz haqimizda malumot",
        facebook="https://facebook.com",
        instagram="https://instagram.com",
        telegram="https://telegram.com",
        email="tohir@gmail.com",
        address="Toshkent",
        is_new_products_show=True,
        is_popular_products_show=True,
        country=country,
        category=shop_category,
        currency=currency,
        owner=user1,
        plan=plan,
    )


@pytest.fixture(scope='function')
def shop2(user2, country, shop_category, currency, plan):
    shop2 = Shop.objects.create(
        name="Shop2 test",
        phone="+998997711310",
        phone_number=None,
        status="active",
        lat=7878700.12,
        lon=7878700.12,
        starts_at=None,
        ends_at=None,
        has_terminal=True,
        about_us="Biz haqimizda malumot",
        facebook="https://facebook.com",
        instagram="https://instagram.com",
        telegram="https://telegram.com",
        email="tohir@gmail.com",
        address="Toshkent",
        is_new_products_show=True,
        is_popular_products_show=True,
        country=country,
        category=shop_category,
        currency=currency,
        owner=user2,
        plan=plan,
    )
    user2.default_shop = shop2
    return shop2


@pytest.fixture(scope='function')
def category(shop):
    CategoryFactory.create_batch(10, **{'shop': shop, 'status': 'active'})
    # return Category.objects.create(
    #     name='Texnika',
    #     emoji='🤑',
    #     position=2,
    #     status='active',
    #     shop=shop
    # )


@pytest.fixture(scope='function')
def category1(shop2):
    return Category.objects.create(
        name='Texnika',
        emoji='🤑',
        position=2,
        status='active',
        shop=shop2
    )


@pytest.fixture(scope='function')
def category2(shop):
    return Category.objects.create(
        name='Iphone',
        emoji='🤑',
        position=2,
        status='active',
        shop=shop
    )


@pytest.fixture(scope='function')
def product(category):
    return Product.objects.create(
        name='Product 1',
        description='chotki',
        category=category,
        full_price=124,
        price=12,
        stock_status='fixed',
        unit='item'
    )


@pytest.fixture(scope='function')
def product1(category1):
    return Product.objects.create(
        name='Product 2',
        description='chotki',
        category=category1,
        full_price=124,
        price=12,
        stock_status='fixed',
        unit='item'
    )


@pytest.fixture(scope='function')
def product2(category):
    return Product.objects.create(
        name='Mahsulot 1',
        description='chotki',
        category=category,
        full_price=124,
        price=12,
        stock_status='fixed',
        unit='item'
    )

import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

from shops.models import Country, ShopCategory, Currency, Shop, Category, Product
from users.models import Plan

# Get the User model
User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')
    is_active = True
    is_superuser = False
    is_staff = True
    type = 'email'


class CountryFactory(DjangoModelFactory):
    class Meta:
        model = Country

    name = factory.Faker('country')
    code = factory.Faker('country_code')


class ShopCategoryFactory(DjangoModelFactory):
    class Meta:
        model = ShopCategory

    name = factory.Faker('word')


class CurrencyFactory(DjangoModelFactory):
    class Meta:
        model = Currency

    name = factory.Faker('currency_name')
    order = factory.Sequence(lambda n: n + 1)


class PlanFactory(DjangoModelFactory):
    class Meta:
        model = Plan

    name = factory.Faker('word')
    code = factory.Faker('slug')
    description = factory.Faker('sentence')


class ShopFactory(DjangoModelFactory):
    class Meta:
        model = Shop

    name = factory.Faker('company')
    phone = factory.Faker('phone_number')
    phone_number = factory.Faker('phone_number')
    status = 'active'
    lat = factory.Faker('latitude')
    lon = factory.Faker('longitude')
    starts_at = None
    ends_at = None
    has_terminal = factory.Faker('boolean')
    about_us = factory.Faker('paragraph')
    facebook = factory.Faker('url')
    instagram = factory.Faker('url')
    telegram = factory.Faker('url')
    email = factory.Faker('email')
    address = factory.Faker('address')
    is_new_products_show = True
    is_popular_products_show = True
    country = factory.SubFactory(CountryFactory)
    category = factory.SubFactory(ShopCategoryFactory)
    currency = factory.SubFactory(CurrencyFactory)
    owner = factory.SubFactory(UserFactory)
    plan = factory.SubFactory(PlanFactory)


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('word')
    emoji = factory.Faker('emoji')
    position = factory.Sequence(lambda n: n + 1)
    status = 'active'
    shop = factory.SubFactory(ShopFactory)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('word')
    description = factory.Faker('sentence')
    category = factory.SubFactory(CategoryFactory)
    full_price = factory.Faker('random_number', digits=5)
    price = factory.Faker('random_number', digits=3)
    stock_status = 'fixed'
    unit = 'item'

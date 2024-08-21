from rest_framework.fields import CurrentUserDefault, HiddenField
from rest_framework.serializers import ModelSerializer
from shops.models import Category, Shop


class ShopModelSerializer(ModelSerializer):
    owner = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Shop
        fields = ('id', 'name', 'category', 'status', 'currency', 'owner')
        read_only_fields = ['owner']


class ShopDetailModelSerializer(ModelSerializer):
    class Meta:
        model = Shop
        exclude = ()


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        exclude = ()
        read_only_fields = ['shop']


class CategoryDetailModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        exclude = ()

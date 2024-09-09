from drf_spectacular.utils import extend_schema_field
from rest_framework.fields import (CurrentUserDefault, HiddenField,
                                   SerializerMethodField,)
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import CharField, ModelSerializer
from shared import DynamicFieldsModelSerializer
from shops.models import Country, Currency, Language, Shop, ShopCategory
from users.models import Plan, PlanPricing, PlanQuotas


class CurrencyModelSerializer(ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"


class CountryModelSerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class LanguageDynamicFieldsModelSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"


class ShopCategoryModelSerializer(ModelSerializer):
    class Meta:
        model = ShopCategory
        fields = "__all__"


class PlanQuotasModelSerializer(ModelSerializer):
    name = SerializerMethodField()

    class Meta:
        model = PlanQuotas
        fields = ('id', 'name', 'value')

    @extend_schema_field(CharField)
    def get_name(self, obj) -> str:
        return obj.quotas.name


class PlanPricingModelSerializer(ModelSerializer):
    class Meta:
        model = PlanPricing
        fields = "__all__"


class PlanModelSerializer(ModelSerializer):
    quotas = PlanQuotasModelSerializer(many=True, read_only=True, source='planquotas_set')
    pricing = PlanPricingModelSerializer(many=True, read_only=True, source='planpricing_set')

    class Meta:
        model = Plan
        fields = ('name', 'code', 'description', 'quotas', 'pricing')


class ShopDynamicFieldsModelSerializer(DynamicFieldsModelSerializer):
    owner = HiddenField(default=CurrentUserDefault())
    plan = PlanModelSerializer(read_only=True)

    class Meta:
        model = Shop
        fields = "__all__"

    def to_representation(self, instance: Shop, *args, **kwargs):
        repr = super().to_representation(instance)
        repr['country'] = CountryModelSerializer(instance.country).data
        repr['languages'] = LanguageDynamicFieldsModelSerializer(
            instance.languages.all(), many=True, fields=['code']).data
        return repr

    def create(self, validated_data):
        validated_data['plan'] = get_object_or_404(Plan, code='free')
        shop = Shop.objects.create(**validated_data)
        user = self.context['request'].user
        user.default_shop = shop
        user.save()
        return shop


class ShopUpdateModelSerializer(ModelSerializer):
    class Meta:
        model = Shop
        exclude = ('owner', 'category', 'services', 'plan', 'starts_at', 'ends_at')
        read__only_fields = ('category', 'services', 'plan')

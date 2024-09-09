from rest_framework.exceptions import PermissionDenied
from shared import DynamicFieldsModelSerializer
from shops.models import Product
from shops.serializers.categories import CategoryDynamicFieldsModelSerializer


class ProductDynamicFieldsModelSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        shop = self.context['shop']
        if shop.owner != self.context['request'].user:
            raise PermissionDenied({'detail': 'You do not have permission to perform this operation.'})
        return super().create(validated_data)

    def to_representation(self, instance: Product):
        repr = super().to_representation(instance)
        repr['category'] = CategoryDynamicFieldsModelSerializer(instance.category).data
        return repr

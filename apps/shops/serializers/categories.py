from rest_framework.exceptions import PermissionDenied
from shared import DynamicFieldsModelSerializer
from shops.models import Category


class CategoryDynamicFieldsModelSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Category
        exclude = ('shop',)

    def create(self, validated_data):
        shop = self.context['shop']
        if shop.owner != self.context['request'].user:
            raise PermissionDenied({'detail': 'You do not have permission to perform this operation.'})
        validated_data['shop'] = shop
        return super().create(validated_data)

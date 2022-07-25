from rest_framework import serializers
from .models import Cart, CartItem


def validate_quantity(value):
    if value <= 0:
        raise serializers.ValidationError('تعداد باید بزرگتر مساوی 1 باشد')


class CartAddRemoveSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True, validators=[validate_quantity])


class CartShowSerializer(serializers.ModelSerializer):

    def get_product(self, obj):
        return {
            'product_id': obj.product.id,
            'product_name': obj.product.name,
            'product_image': self.context['request'].build_absolute_uri(obj.product.image.url),
        }

    product = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('price', 'quantity', 'product')

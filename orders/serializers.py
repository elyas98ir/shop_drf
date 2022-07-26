from rest_framework import serializers
from .models import Cart, CartItem
from .validators import validate_quantity, validate_code, validate_coupon_code
from accounts.validators import validate_phone_number
from .inc import check_coupon_validation, create_new_order


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


class CheckCouponSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)

    def check_coupon(self, validated_data):
        return check_coupon_validation(validated_data['code'])


class OrderCheckoutSerializer(serializers.Serializer):
    recipient_name = serializers.CharField(required=True)
    recipient_phone_number = serializers.CharField(required=True, validators=[validate_phone_number])
    recipient_address = serializers.CharField(required=True)
    coupon_code = serializers.CharField(required=False, validators=[validate_coupon_code])

    def create_order(self, validated_data):
        if 'coupon_code' not in validated_data:
            validated_data['coupon_code'] = None
        return create_new_order(self.context['request'], validated_data['recipient_name'],
                                validated_data['recipient_phone_number'],
                                validated_data['recipient_address'], validated_data['coupon_code'])

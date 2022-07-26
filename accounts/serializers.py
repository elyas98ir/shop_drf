from rest_framework import serializers
from .models import OTPCode, User, Address
import random
from django.utils import timezone
from datetime import timedelta
from .inc import create_code, verify_code
from .validators import validate_phone_number, validate_first_name, validate_last_name, validate_zipcode
from orders.models import Order, Payment


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, validators=[validate_phone_number])

    def create_otp(self, validated_data):
        return create_code(validated_data['phone_number'])


class OTPCodeSerializer(serializers.ModelSerializer):

    def get_status(self, obj):
        if User.objects.filter(phone_number=obj.phone_number).exists():
            return 'old_user'
        else:
            return 'new_user'

    status = serializers.SerializerMethodField()

    class Meta:
        model = OTPCode
        fields = ('phone_number', 'code', 'status')
        extra_kwargs = {
            'phone_number': {'validators': [validate_phone_number]}
        }

    def verify_otp(self, validated_data):
        return verify_code(validated_data['phone_number'], validated_data['code'])


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'image')
        extra_kwargs = {
            'phone_number': {'read_only': True},
            'first_name': {'validators': [validate_first_name]},
            'last_name': {'validators': [validate_last_name]},
        }


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'state', 'city', 'address', 'zipcode')
        extra_kwargs = {
            'zipcode': {'validators': [validate_zipcode]}
        }


class UserOrdersSerializer(serializers.ModelSerializer):

    def get_total_amount(self, obj):
        return obj.get_total_cost(without_discount=True)

    def get_total_payment(self, obj):
        return obj.get_total_cost(without_discount=False)

    def get_order_items(self, obj):
        order_items = []
        for item in obj.items.all():
            order_items.append({
                'product_name': item.product.name,
                'product_price': item.price,
                'product_image': self.context['request'].build_absolute_uri(item.product.image.url),
                'quantity': item.quantity,
            })
        return order_items

    total_amount = serializers.SerializerMethodField()
    total_payment = serializers.SerializerMethodField()
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'recipient_name', 'recipient_phone_number', 'recipient_address', 'coupon_code',
                  'coupon_discount', 'paid', 'updated', 'total_amount', 'total_payment', 'order_items')


class UserPaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'order', 'amount', 'status', 'tracking_code', 'updated')

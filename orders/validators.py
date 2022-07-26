from rest_framework import serializers
from .inc import get_coupon


def validate_quantity(value):
    if value <= 0:
        raise serializers.ValidationError('تعداد باید بزرگتر مساوی 1 باشد')


def validate_code(value):
    if len(code) <= 0:
        raise serializers.ValidationError('کد تخفیف باید حداقل 1 کاراکتر باشد')


def validate_coupon_code(value):
    if len(value) > 0:
        coupon = get_coupon(value)
        if coupon is None:
            raise serializers.ValidationError('کد تخفیف وارد شده معتبر نمیباشد')

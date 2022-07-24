from rest_framework import serializers
from .models import OTPCode, User
import random
from django.utils import timezone
from datetime import timedelta
from .inc import create_code, verify_code


def validate_phone_number(value):
    if len(value) != 11 or not value.startswith('09'):
        raise serializers.ValidationError('شماره تلفن وارد شده معتبر نمیباشد')
    return value


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

from rest_framework import serializers


def validate_phone_number(value):
    if len(value) != 11 or not value.startswith('09'):
        raise serializers.ValidationError('شماره تلفن وارد شده معتبر نمیباشد')
    return value


def validate_first_name(value):
    if len(value) < 3:
        raise serializers.ValidationError('نام باید حداقل 3 کاراکتر باشد')


def validate_last_name(value):
    if len(value) < 3:
        raise serializers.ValidationError('نام خانوادگی باید حداقل 3 کاراکتر باشد')

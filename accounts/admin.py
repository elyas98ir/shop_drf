from django.contrib import admin
from .models import User, OTPCode, Address


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'email')


@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'state', 'city', 'address', 'zipcode')

from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ('product',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', 'updated')
    inlines = (CartItemInline,)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'paid', 'created', 'updated')
    inlines = (OrderItemInline,)

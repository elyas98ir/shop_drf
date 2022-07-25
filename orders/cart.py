from .models import Cart, CartItem
from products.models import Product
from django.shortcuts import get_object_or_404
from rest_framework import status


def get_cart(request):
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user)

    return cart


def check_quantity(product, quantity):
    if product.stock_quantity >= quantity:
        return 'add'
    return {
        'err': 'stock_quantity_error',
        'msg': 'تعداد درخواستی بیشتر از موجودی انبار میباشد'
    }, status.HTTP_400_BAD_REQUEST


def add(request, validated_data):
    cart = get_cart(request)
    product = get_object_or_404(Product, pk=validated_data['product_id'])

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        new_quantity = cart_item.quantity + validated_data['quantity']
        res = check_quantity(product, new_quantity)
        if res == 'add':
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            return res

    except CartItem.DoesNotExist:
        res = check_quantity(product, validated_data['quantity'])
        if res == 'add':
            cart.items.create(cart=cart, product=product, price=product.price,
                              quantity=validated_data['quantity'])
        else:
            return res

    return {
        'err': 'cart_add_successfully',
        'msg': 'آیتم با موفقیت اضافه/درج شد'
    }, status.HTTP_200_OK


def remove(request, validated_data):
    cart = get_cart(request)
    product = get_object_or_404(Product, pk=validated_data['product_id'])

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        new_quantity = cart_item.quantity - validated_data['quantity']
        if new_quantity >= 1:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            cart_item.delete()

        if cart.items.count() == 0:
            cart.delete()

    except CartItem.DoesNotExist:
        return {
            'err': 'cart_item_error',
            'msg': 'یافت نشد'
        }, status.HTTP_400_BAD_REQUEST

    return {
        'err': 'cart_remove_successfully',
        'msg': 'آیتم با موفقیت کم/حذف شد'
    }, status.HTTP_204_NO_CONTENT


def show(request):
    cart = get_cart(request)
    if cart:
        return cart.items.all()

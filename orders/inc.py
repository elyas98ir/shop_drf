from .models import Coupon
from django.utils import timezone
from rest_framework import status
from .models import Order, OrderItem, Cart, CartItem


def get_coupon(code):
    now = timezone.now()
    try:
        return Coupon.objects.get(code__exact=code, valid_to__gte=now, active=True)
    except Coupon.DoesNotExist:
        return None


def check_coupon_validation(code):
    now = timezone.now()
    coupon = get_coupon(code)
    if coupon:
        return {
            'code': coupon.code,
            'discount': coupon.discount,
            'msg': f'مقدار این کد تخفیف {coupon.discount} درصد میباشد'
        }, status.HTTP_200_OK
    else:
        return {
            'err': 'code_not_found',
            'msg': 'کد تخفیف وارد شده معتبر نیست'
        }, status.HTTP_404_NOT_FOUND


def create_new_order(context, recipient_name, recipient_phone_number,
                     recipient_address, coupon_code):
    user = context.user
    Order.objects.filter(user=user, paid=False).delete()

    if coupon_code is not None:
        coupon = get_coupon(coupon_code)

    cart = Cart.objects.get(user=user)
    order = Order.objects.create(user=user, recipient_name=recipient_name,
                                 recipient_phone_number=recipient_phone_number,
                                 recipient_address=recipient_address,
                                 coupon_code=coupon.code if coupon_code is not None else None,
                                 coupon_discount=coupon.discount if coupon_code is not None else None)

    order_items = []
    for item in cart.items.all():
        OrderItem.objects.create(order=order, product=item.product,
                                 price=item.product.price, quantity=item.quantity)
        order_items.append({
            'product_name': item.product.name,
            'product_price': item.product.price,
            'product_image': context.build_absolute_uri(item.product.image.url),
            'quantity': item.quantity,
        })

    return {
        'recipient_name': order.recipient_name,
        'recipient_phone_number': order.recipient_phone_number,
        'recipient_address': order.recipient_address,
        'total_amount': order.get_total_cost(without_discount=True),
        'payment_amount': order.get_total_cost(without_discount=False),
        'coupon_code': order.coupon_code,
        'coupon_discount': order.coupon_discount,
        'order_items': order_items
    }, status.HTTP_200_OK

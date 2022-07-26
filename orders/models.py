from django.db import models
from accounts.models import User, Address
from products.models import Product


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart', verbose_name='کاربر')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد خرید'

    def __str__(self):
        return f'سبد خرید - {self.user}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    price = models.PositiveIntegerField(verbose_name='قیمت')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'آیتم‌های سبد خرید'
        verbose_name_plural = 'آیتم‌های سبد خرید'

    def __str__(self):
        return f'آیتم‌های {self.cart}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='کاربر')
    recipient_name = models.CharField(max_length=100, verbose_name='نام گیرنده')
    recipient_phone_number = models.CharField(max_length=11, verbose_name='شماره تماس گیرنده')
    recipient_address = models.CharField(max_length=250, verbose_name='آدرس گیرنده')
    coupon_code = models.CharField(max_length=20, default=None, null=True, blank=True, verbose_name='کد تخفیف')
    coupon_discount = models.PositiveSmallIntegerField(default=None, null=True, blank=True, verbose_name='درصد تخفیف')
    paid = models.BooleanField(default=False, verbose_name='وضعیت پرداخت')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        ordering = ('paid', '-id',)
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

    def __str__(self):
        return f'سفارش - {self.user}'

    def get_total_cost(self, without_discount):
        total = sum(item.get_item_cost() for item in self.items.all())
        total_with_discount = total

        if self.coupon_code and self.coupon_discount:
            discount_price = (self.coupon_discount / 100) * total
            total_with_discount = int(total - discount_price)

        if without_discount:
            return total
        return total_with_discount


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    price = models.PositiveIntegerField(verbose_name='قیمت')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        ordering = ('id',)
        verbose_name = 'آیتم‌های سفارش'
        verbose_name_plural = 'آیتم‌های سفارش'

    def __str__(self):
        return f'آیتم‌های {self.order}'

    def get_item_cost(self):
        return self.price * self.quantity


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                             blank=True, related_name='user', verbose_name='کاربر')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True,
                              blank=True, related_name='order', verbose_name='سفارش')
    amount = models.PositiveIntegerField(verbose_name='مبلغ')
    authority = models.CharField(max_length=250, verbose_name='کد پرداخت')
    status = models.BooleanField(default=False, verbose_name='وضعیت')
    tracking_code = models.CharField(max_length=100, default=None, null=True, blank=True, verbose_name='کد رهگیری')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        ordering = ('status', '-id')
        verbose_name = 'تراکنش'
        verbose_name_plural = 'تراکنش‌ها'

    def __str__(self):
        return f'{self.tracking_code} - {self.status}'


class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name='کد تخفیف')
    discount = models.PositiveSmallIntegerField(verbose_name='درصد تخفیف')
    valid_to = models.DateTimeField(verbose_name='تاریخ انقضا')
    active = models.BooleanField(default=True, verbose_name='وضعیت')

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کد تخفیف'

    def __str__(self):
        return f'{self.code} - {self.discount}'

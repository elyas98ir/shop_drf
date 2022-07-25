from django.db import models
from accounts.models import User
from products.models import Product


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart', verbose_name='کاربر')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        ordering = ('id',)
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
        ordering = ('id',)
        verbose_name = 'آیتم‌های سبد خرید'
        verbose_name_plural = 'آیتم‌های سبد خرید'

    def __str__(self):
        return f'آیتم‌های {self.cart}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order', verbose_name='کاربر')
    paid = models.BooleanField(default=False, verbose_name='وضعیت پرداخت')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        ordering = ('id',)
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

    def __str__(self):
        return f'سفارش - {self.user}'

    def get_total_cost(self):
        return sum(item.get_item_cost() for item in self.items.all())


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
        return f'آیتم‌های {self.cart}'

    def get_item_cost(self):
        return self.price * self.quantity

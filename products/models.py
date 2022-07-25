from django.db import models
from .managers import CategoryManager, ProductManager


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name='نام')
    slug = models.SlugField(max_length=250, unique=True, verbose_name='اسلاگ')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='children', verbose_name='دسته‌بندی مادر')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    objects = CategoryManager()

    class Meta:
        ordering = ('-id',)
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products', verbose_name='دسته‌بندی')
    name = models.CharField(max_length=250, verbose_name='نام')
    slug = models.SlugField(max_length=250, unique=True, verbose_name='اسلاگ')
    image = models.ImageField(upload_to='products/images/', verbose_name='تصویر محصول')
    description = models.TextField(verbose_name='توضیحات')
    price = models.PositiveIntegerField(verbose_name='قیمت')
    stock_quantity = models.PositiveIntegerField(verbose_name='تعداد موجودی در انبار')
    available = models.BooleanField(default=True, verbose_name='وضعیت')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    objects = ProductManager()

    class Meta:
        ordering = ('-id',)
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.name

    def categories(self):
        return ', '.join([category.name for category in self.category.all()])
    categories.short_description = 'دسته‌بندی‌ها'

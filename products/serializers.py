from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'parent')


class ProductSerializer(serializers.ModelSerializer):

    def get_categories(self, obj):
        cats = []
        for cat in obj.category.all():
            cats.append({
                'id': cat.id,
                'name': cat.name,
            })
        return cats

    categories = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'description', 'image', 'price', 'stock_quantity', 'categories', 'category')
        extra_kwargs = {
            'category': {'write_only': True}
        }

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from .models import Category, Product
from . import serializers
from .permissions import IsAdminOrReadOnly


class CaregoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class CategoryMainView(ListAPIView):
    queryset = Category.objects.main_categories()
    serializer_class = serializers.CategorySerializer


class CategoryChildrenView(ListAPIView):
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return category.children


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.availables()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAdminOrReadOnly]


class CategoryProductView(ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return category.products

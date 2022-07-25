from django.urls import path
from rest_framework import routers
from . import views

app_name = 'products'

urlpatterns = [
    path('categories/main/', views.CategoryMainView.as_view(), name='category_main'),
    path('categories/<int:pk>/children/', views.CategoryChildrenView.as_view(), name='category_children'),
    path('categories/<int:pk>/products/', views.CategoryProductView.as_view(), name='category_products')
]

router = routers.SimpleRouter()
router.register('categories', views.CaregoryViewSet, basename='categories')
router.register('products', views.ProductViewSet, basename='products')
urlpatterns += router.urls

from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    path('cart/', views.CartShowView.as_view(), name='cart_show'),
    path('cart/add/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/remove/', views.CartRemoveView.as_view(), name='cart_remove'),
    path('cart/clear/', views.CartClearView.as_view(), name='cart_clear'),
]

from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    path('cart/', views.CartShowView.as_view(), name='cart_show'),
    path('cart/add/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/remove/', views.CartRemoveView.as_view(), name='cart_remove'),
    path('cart/clear/', views.CartClearView.as_view(), name='cart_clear'),
    path('order/coupon/', views.CheckCouponView.as_view(), name='check_coupon'),
    path('order/checkout/', views.OrderCheckoutView.as_view(), name='order_checkout'),
    path('order/pay/send/', views.OrderPaySend.as_view(), name='pay_send'),
    path('order/pay/verify/', views.OrderPayVerify.as_view(), name='pay_verify'),
]

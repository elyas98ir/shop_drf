from django.urls import path
from . import views
from rest_framework import routers

app_name = 'accounts'

urlpatterns = [
    path('otp/', views.OTPCodeView.as_view(), name='otp'),
    path('user/profile/', views.UserProfile.as_view(), name='profile'),
    path('user/orders/', views.UserOrdersView.as_view(), name='user_orders'),
    path('user/payments/', views.UserPaymentsView.as_view(), name='user_payments'),
]

router = routers.SimpleRouter()
router.register('user/address', views.AddressViewSet, basename='address')
urlpatterns += router.urls

from django.urls import path
from . import views
from rest_framework import routers

app_name = 'accounts'

urlpatterns = [
    path('otp/', views.OTPCodeView.as_view(), name='otp'),
    path('user/profile/', views.UserProfile.as_view(), name='profile'),
]

router = routers.SimpleRouter()
router.register('user/address', views.AddressViewSet, basename='address')
urlpatterns += router.urls

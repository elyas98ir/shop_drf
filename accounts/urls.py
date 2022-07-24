from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('otp/', views.OTPCodeView.as_view(), name='otp'),
]

from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from rest_framework import status
from . import serializers
from .models import User, Address
from orders.models import Order, Payment


class OTPCodeView(APIView):
    def get(self, request):
        phone_number = request.query_params['phone_number']
        srz_data = serializers.PhoneNumberSerializer(data={'phone_number': phone_number})
        if srz_data.is_valid():
            result = srz_data.create_otp(srz_data.validated_data).data
            return Response(data=result, status=status.HTTP_201_CREATED)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        srz_data = serializers.OTPCodeSerializer(data=request.data)
        if srz_data.is_valid():
            result, status_code = srz_data.verify_otp(srz_data.validated_data)
            return Response(data=result, status=status_code)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(RetrieveUpdateAPIView):
    def get_object(self):
        return self.request.user

    serializer_class = serializers.UserProfileSerializer
    permission_classes = [IsAuthenticated]


class AddressViewSet(ModelViewSet):
    serializer_class = serializers.AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserOrdersView(ListAPIView):
    serializer_class = serializers.UserOrdersSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, paid=True)


class UserPaymentsView(ListAPIView):
    serializer_class = serializers.UserPaymentsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

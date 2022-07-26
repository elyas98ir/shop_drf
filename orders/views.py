from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . import pay
from .models import Cart, CartItem, Order, Payment
from . import cart
from . import serializers


class CartShowView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CartShowSerializer

    def get_queryset(self):
        return cart.show(self.request)


class CartAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        srz_data = serializers.CartAddRemoveSerializer(data=request.data)
        if srz_data.is_valid():
            result, status_code = cart.add(request, srz_data.validated_data)
            return Response(data=result, status=status_code)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class CartRemoveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        srz_data = serializers.CartAddRemoveSerializer(data=request.data)
        if srz_data.is_valid():
            result, status_code = cart.remove(request, srz_data.validated_data)
            return Response(data=result, status=status_code)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class CartClearView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CartShowSerializer

    def get_object(self):
        return cart.get_cart(self.request)


class CheckCouponView(APIView):
    def get(self, request):
        code = request.query_params['code']
        srz_data = serializers.CheckCouponSerializer(data={'code': code})
        if srz_data.is_valid():
            result, status_code = srz_data.check_coupon(srz_data.validated_data)
            return Response(data=result, status=status_code)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderCheckoutView(APIView):
    def post(self, request):
        srz_data = serializers.OrderCheckoutSerializer(data=request.data, context={'request': request})
        if srz_data.is_valid():
            result, status_code = srz_data.create_order(srz_data.validated_data)
            return Response(data=result, status=status_code)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderPaySend(APIView):
    def post(self, request):
        order = Order.objects.get(user=request.user, paid=False)
        return pay.send(user=request.user, order=order)


class OrderPayVerify(APIView):
    def get(self, request):
        return pay.verify(request=request)

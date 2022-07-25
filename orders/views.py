from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
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

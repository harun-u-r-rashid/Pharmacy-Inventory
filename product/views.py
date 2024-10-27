from django.shortcuts import render
from .models import Product, Purchase, Sell
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from user.models import User


from .serializers import ProductSerializer, PurchaseSerializer, SellSerializer


class ProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_product = serializer.save()
        new_product.save()


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        update_course = serializer.save()


class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


# Purchase


class PurchaseCreateView(generics.CreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [AllowAny]


    def create(self, request, *args, **kwargs):
        purchase_id = request.data.get("purchase_id")
        user_id = request.data.get("user")
        product_id = request.data.get("product")
        quantity = request.data.get("quantity")

        if not all([purchase_id, user_id, product_id, quantity]):
            return Response(
                {"message": "Missing fields in request data"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        

        user = User.objects.filter(id=user_id).first()

        product = Product.objects.filter(id=product_id).first()

        if not user or not product:
            return Response(
                {"message": "User or Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        purchase = Purchase.objects.filter(purchase_id=purchase_id).first()

        if user.is_staff:

            if purchase:
                product.quantity += quantity
                purchase.quantity += quantity
                purchase.save()
                product.save()
                return Response(
                    {"message": "Purchase updated successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                purchase = Purchase(
                    purchase_id=purchase_id,
                    product=product,
                    user=user,
                    quantity=quantity,
                )
                purchase.save()
                product.quantity += quantity
                product.save()
                return Response(
                    {"message": "Purchase created successfully"},
                    status=status.HTTP_201_CREATED,
                )
        else:
            return Response(
                    {"message": "Only staff user can purchase the product."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            
class SellCreateView(generics.CreateAPIView):
    queryset = Sell.objects.all()
    serializer_class = SellSerializer
    permission_classes = [AllowAny]


    def create(self, request, *args, **kwargs):
        sell_id = request.data.get("sell_id")
        user_id = request.data.get("user")
        product_id = request.data.get("product")
        quantity = request.data.get("quantity")

        if not all([sell_id, user_id, product_id, quantity]):
            return Response(
                {"message": "Missing fields in request data"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        

        user = User.objects.filter(id=user_id).first()

        product = Product.objects.filter(id=product_id).first()

        if not user or not product:
            return Response(
                {"message": "User or Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        sell = Sell.objects.filter(sell_id=sell_id).first()

        if user.is_staff:

            if sell:
                product.quantity -= quantity
                sell.quantity += quantity
                product.save()
                sell.save()
                return Response(
                    {"message": "Sell updated successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                sell = Sell(
                    sell_id=sell_id,
                    product=product,
                    user=user,
                    quantity=quantity,
                )
                sell.save()
                product.quantity -= quantity
                product.save()
                return Response(
                    {"message": "Sell created successfully"},
                    status=status.HTTP_201_CREATED,
                )
        else:
            return Response(
                    {"message": "Only staff user can sell the product."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            



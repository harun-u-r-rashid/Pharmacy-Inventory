from django.shortcuts import render # type: ignore
from .models import Product, Purchase, Sell
from rest_framework import generics # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from rest_framework.exceptions import PermissionDenied # type: ignore

from user.models import User


from .serializers import ProductSerializer, PurchaseSerializer, SellSerializer

# View for Product
class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_is_staff = self.request.user.is_staff

        if not user_is_staff:
            raise PermissionDenied("Only staff user can view the product.")
        return Product.objects.all().order_by("-id")


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_is_staff = request.user.is_staff
        if user_is_staff:
            if isinstance(request.data, list):
                serializer = self.get_serializer(data=request.data, many=True)
            else:
                serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"message": "Only staff user can create product."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def perform_create(self, serializer):
        serializer.save()


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):

        user_is_staff = self.request.user.is_staff
        # print(user_is_staff)

        if not user_is_staff:
            raise PermissionDenied("Only staff users can update products.")

        update_course = serializer.save()


class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):

        user_is_staff = self.request.user.is_staff

        if not user_is_staff:
            raise PermissionDenied("Only staff can delete a product.")
        return super().destroy(request, *args, **kwargs)


# View for Purchase
class PurchaseListView(generics.ListAPIView):
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_is_staff = self.request.user.is_staff

        if not user_is_staff:
            raise PermissionDenied("Only staff can view the purchased product")
        return Purchase.objects.all().order_by("-id")

class PurchaseCreateView(generics.CreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_is_staff = self.request.user.is_staff

        if not user_is_staff:
            return Response(
                {"message": "Only staff users can make purchases."},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data if isinstance(request.data, list) else [request.data]

        for purchase_data in data:
            user_id = purchase_data.get("user")
            product_id = purchase_data.get("product")
            quantity = purchase_data.get("quantity")

            if not all([user_id, product_id, quantity]):
                return Response(
                    {"message": "Missing fields in purchase data"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.filter(id=user_id).first()
            if not user:
                return Response(
                    {"message": "User not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            product = Product.objects.filter(id=product_id).first()
            if not product:
                return Response(
                    {"message": f"Product with ID {product_id} not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            purchase = Purchase(
                product=product,
                user=user,
                quantity=quantity,
            )
            purchase.save()
            product.quantity += quantity
            product.save()

        return Response(
            {"message": "Purchase processed successfully for multiple products."},
            status=status.HTTP_201_CREATED,
        )


# View for Sell
class SellListView(generics.ListAPIView):
    serializer_class = SellSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_is_staff = self.request.user.is_staff

        if not user_is_staff:
            raise PermissionDenied("Only staff can view the sold product")
        return Sell.objects.all().order_by("-id")

class SellCreateView(generics.CreateAPIView):
    queryset = Sell.objects.all()
    serializer_class = SellSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_is_staff = self.request.user.is_staff

        if not user_is_staff:
            return Response(
                {"message": "Only staff users can sell."},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data if isinstance(request.data, list) else [request.data]

        for purchase_data in data:
            user_id = purchase_data.get("user")
            product_id = purchase_data.get("product")
            quantity = purchase_data.get("quantity")

            if not all([user_id, product_id, quantity]):
                return Response(
                    {"message": "Missing fields in purchase data"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.filter(id=user_id).first()
            if not user:
                return Response(
                    {"message": "User not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            product = Product.objects.filter(id=product_id).first()
            if not product:
                return Response(
                    {"message": f"Product with ID {product_id} not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            purchase = Sell(
                product=product,
                user=user,
                quantity=quantity,
            )
            purchase.save()
            product.quantity -= quantity
            product.save()

        return Response(
            {"message": "Product sold successfully."},
            status=status.HTTP_201_CREATED,
        )

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .utils import send_code_to_user
from rest_framework.permissions import AllowAny, IsAuthenticated


from user.models import OneTimePassword
from django.contrib.auth import authenticate

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from user.models import User
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer, OTPCodeSerializer, ProductSerializer, PurchaseSerializer, SellSerializer





class RegistrationView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


    def post(self, request):
        print(request.data)

        user = request.data
        serializer = RegisterSerializer(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data = serializer.data

            send_code_to_user(user_data["email"])
            return Response(
                {
                    "data": user_data,
                    "message": "A passcode has been sent to your email",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VerifyUserView(APIView):
    permission_classes = [AllowAny]
    serializer_class = OTPCodeSerializer


    def post(self, request):
        serializer = OTPCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp_code = serializer.validated_data.get("otp")

        try:
            user_code_obj = OneTimePassword.objects.get(code=otp_code)
            user = user_code_obj.user
            if not user.is_active:
                user.is_active = True
                user.save()
                return Response(
                    {"message": "Account email verified successfully!"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"message": "Code is not valid"}, status=status.HTTP_204_NO_CONTENT
            )
        except OneTimePassword.DoesNotExist:
            return Response(
                {"message": "Passcode not provided"}, status=status.HTTP_400_BAD_REQUEST
            )
        
class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        print("responce", request.data)
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.data
        return Response(status=status.HTTP_200_OK)




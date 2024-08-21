from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import User
from users.serializers import (EmptySerializer, LoginSerializer,
                               ResetPasswordSerializer, UserSerializer, PasswordResetConfirmSerializer, )
from users.tasks import send_email
from users.tokens import account_activation_token

User = get_user_model()


class RegisterUserView(GenericAPIView):
    serializer_class = UserSerializer

    @extend_schema(
        request=UserSerializer,
        description='Register a new user with first name, last name, email, password, and password confirmation.',
        summary='User Registration',
        tags=['Auth'],
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Trigger the email confirmation task
            send_email.delay(user.id, is_reset_password=False, base_url=settings.BASE_URL)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailConfirmationView(GenericAPIView):
    @extend_schema(
        description='Confirm a user’s email address by verifying the provided token.',
        summary='Email Confirmation',
        tags=['Auth'],
    )
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid user ID.'}, status=status.HTTP_400_BAD_REQUEST)

        if account_activation_token.check_token(user, token):
            # Here you can mark the user as confirmed or activated
            user.is_active = True
            user.save()
            return Response({'detail': 'Email has been confirmed successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(GenericAPIView):
    serializer_class = LoginSerializer

    @extend_schema(
        request=LoginSerializer,
        description='Log in a user with email and password to receive an authentication token.',
        summary='User Login',
        tags=['Auth'],
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)

            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)

            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    @extend_schema(
        description='Log out the current user by deleting their authentication token.',
        summary='User Logout',
        tags=['Auth'],
    )
    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'error': 'Token not found.'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    @extend_schema(
        request=ResetPasswordSerializer,
        description='Request a password reset for a user by providing their email address.',
        summary='Password Reset',
        tags=['Auth'],
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.send_reset_email()
            return Response({'detail': 'Password reset email sent.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    @extend_schema(
        request=PasswordResetConfirmSerializer,
        description='Confirm a password reset by providing the token, email, and new password.',
        summary='Password Reset Confirmation',
        tags=['Auth'],
    )
    def post(self, request, uidb64=None, token=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data.get('new_password')

            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return Response({'error': 'Invalid user ID.'}, status=status.HTTP_400_BAD_REQUEST)

            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

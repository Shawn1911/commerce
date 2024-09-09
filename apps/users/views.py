import uuid

from django.contrib.auth import authenticate
from django.core.cache import cache
from django.template.loader import render_to_string
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (GenericAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404,)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from shared import translate_message, unique_code
from users.models import User
from users.serializers import (AuthModelSerializer, ConfirmEmailSerializer,
                               EnterYourEmailSerializer, LoginSerializer,
                               LogoutSerializer, SignUpModelSerializer,
                               UpdatePasswordSerializer,
                               UserDefaultShopUpdateSerializer,)
from users.tasks import send_email


@extend_schema(tags=['users'])
class SingUpCreateAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpModelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=['auth'])
class ConfirmEmailAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ConfirmEmailSerializer

    def get(self, request, token):
        serializer = self.serializer_class(data={'token': token})
        serializer.is_valid(raise_exception=True)
        if user := get_object_or_404(User, email=cache.get(token)):
            user.is_active = True
            user.is_staff = True
            user.invitation_code = unique_code()
            user.public_offer = True
            user.save()
            return Response({"message": "User activated successfully!"})
        return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['auth'])
class LoginAPIView(GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @action(detail=False, methods=['post'])
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(email=email, password=password, is_active=True)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['auth'])
class ForgotPasswordAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EnterYourEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        token = str(uuid.uuid4())
        language = request.header.get('language')
        scheme = request.scheme
        host = request.get.host()
        context = {
            'confirmation_url': f"{scheme}://{host}/api/v1/users/reset-password/{token}",
            'type': 'change_password',
            'language': language,
            'home_url': f"{scheme}://{host}",
        }
        message = render_to_string(
            template_name="link.html",
            context=context
        )
        send_email.delay(email, message, translate_message(language))
        cache.set(token, email, 300)
        return Response({"message": "Email sent successfully!"}, status.HTTP_200_OK)


@extend_schema(tags=['users'])
class UpdatePasswordAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UpdatePasswordSerializer

    def post(self, request, token, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if user := get_object_or_404(User, email=cache.get(token)):
            if serializer.validated_data['password'] != serializer.validated_data['confirm_password']:
                raise ValidationError({"password": "Password did not match."})
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({"message": "Password updated successfully!"}, status.HTTP_200_OK)
        return Response({"error": "User does not exist"}, status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['users'])
class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserDefaultShopUpdateSerializer

    def get_object(self):
        return self.request.user


@extend_schema(tags=['auth'])
class AuthRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = AuthModelSerializer

    def get_object(self):
        return self.request.user


@extend_schema(tags=['auth'])
class AuthLogoutAPIView(APIView):
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        token = get_object_or_404(Token, user=request.user)
        token.delete()
        return Response(status=status.HTTP_200_OK)

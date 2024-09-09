import uuid

from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from drf_spectacular.utils import extend_schema_field
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import (CharField, EmailField, IntegerField,
                                        ModelSerializer, Serializer,
                                        ValidationError,)
from rest_framework.validators import UniqueValidator
from shared import translate_message
from shops.models import Shop
from users.models import User, UserLinkedAccount
from users.tasks import send_email


class SignUpModelSerializer(ModelSerializer):
    email = EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email already registered.")]
    )
    password1 = CharField(
        min_length=8, required=True, write_only=True, validators=[validate_password]
    )
    password2 = CharField(
        min_length=8, required=True, write_only=True
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'invitation_code', 'language']
        read_only_fields = ['invitation_code', 'language']

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        validated_data['type'] = User.Type.EMAIL
        user = User(**validated_data)
        user.set_password(password)  # Ensure password is hashed
        user.save()

        UserLinkedAccount.objects.bulk_create(
            [
                UserLinkedAccount(user=user, linked_id=1),
                UserLinkedAccount(user=user, linked_id=2),
            ]
        )

        token = str(uuid.uuid4())
        language = self.context['request'].headers.get('language')
        context = self.get_context(self.context, language, token)
        message = render_to_string("link.html", context)
        send_email.delay(user.email, message, translate_message(language))
        cache.set(token, user.email, 300)

        return user

    def get_context(self, context, language, token):
        scheme = context['request'].scheme
        host = context['request'].get_host()
        return {
            "confirmation_url": f"{scheme}://{host}/api/v1/confirm-email/{token}",
            'type': 'register',
            'language': language,
            'home_url': f"{scheme}://{host}/",
        }


class LoginSerializer(Serializer):
    email = EmailField(required=True, max_length=50)
    password = CharField(required=True, max_length=50, write_only=True)


class EnterYourEmailSerializer(Serializer):
    email = EmailField(required=True, max_length=50)


class UpdatePasswordSerializer(Serializer):
    password = CharField(required=True, max_length=50, write_only=True)
    confirm_password = CharField(required=True, max_length=50, write_only=True)


class UserDefaultShopUpdateSerializer(Serializer):
    shop_id = IntegerField(required=True, write_only=True)

    def update(self, instance, validated_data):
        shop = get_object_or_404(Shop.objects.all(), pk=validated_data['shop_id'])
        instance.default_shop = shop
        instance.save()
        return instance


class UserLinkedAccountModelSerializer(ModelSerializer):
    linked_name = SerializerMethodField()

    class Meta:
        model = UserLinkedAccount
        fields = ['status', 'linked', 'linked_name']

    @extend_schema_field(CharField)
    def get_linked_name(self, obj) -> str:
        return obj.linked_name


class AuthModelSerializer(ModelSerializer):
    linked_account = UserLinkedAccountModelSerializer(source='accounts', many=True)
    token = SerializerMethodField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'type', 'invitation_code', 'public_offer',
                  'default_shop', 'language', 'linked_account', 'token')

    @extend_schema_field(CharField)
    def get_token(self, obj) -> str:
        return obj.auth_token.key


class ConfirmEmailSerializer(Serializer):
    token = CharField()


class LogoutSerializer(Serializer):
    pass

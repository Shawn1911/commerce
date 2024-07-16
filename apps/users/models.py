from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import CharField, ForeignKey, CASCADE, TextField, IntegerField, FloatField, BooleanField, \
    DateTimeField, OneToOneField, EmailField, SET_NULL, BigIntegerField, TextChoices

from shared import CreatedBaseModel


class User(AbstractBaseUser, PermissionsMixin):  # ✅
    class Type(TextChoices):
        EMAIL = 'email', 'Email'
        TELEGRAM = 'telegram', 'Telegram'
        FACEBOOK = 'facebook', 'Facebook'

    type = CharField(max_length=25)
    username = CharField(max_length=150, validators=[UnicodeUsernameValidator()])
    first_name = CharField(max_length=150, blank=True)
    last_name = CharField(max_length=150, blank=True)
    email = EmailField(blank=True)
    is_staff = BooleanField(default=False)
    is_active = BooleanField(default=False)
    is_blocked = BooleanField(db_default=False)
    last_activity = DateTimeField(auto_now_add=True)
    language = ForeignKey('shops.Language', CASCADE)
    public_offer = BooleanField(default=False)
    invitation_code = CharField(max_length=25, unique=True, null=True)
    created_at = DateTimeField(auto_now=True)
    telegram_id = BigIntegerField(blank=True, null=True)
    default_shop = OneToOneField('shops.Shop', SET_NULL, blank=True, null=True)
    shop = ForeignKey('shops.Shop', CASCADE, blank=True, null=True, related_name='customers')

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        unique_together = [
            ('username', 'shop')
        ]


class Plan(CreatedBaseModel):
    code = CharField(max_length=150)
    name = CharField(max_length=150)
    description = TextField(max_length=150)


class PlanPricing(CreatedBaseModel):
    price = FloatField(default=0.0)
    original_price = FloatField(default=0.0)
    name = CharField(max_length=50)
    period = IntegerField(default=30)
    currency = OneToOneField('shops.Currency', CASCADE)
    plan = ForeignKey('shops.Plan', CASCADE)


class PlanQuotas(CreatedBaseModel):
    name = CharField(max_length=150)
    description = TextField(null=True, blank=True)
    value = CharField(max_length=50, null=True, blank=True)
    plan = ForeignKey('shops.Plan', CASCADE)

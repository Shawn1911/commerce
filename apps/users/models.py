from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import CharField, ForeignKey, CASCADE, TextField, IntegerField, FloatField, BooleanField, \
    DateTimeField, OneToOneField, EmailField

from shared import CreatedBaseModel


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = CharField(max_length=150, unique=True, validators=[username_validator])
    first_name = CharField(max_length=150, blank=True)
    last_name = CharField(max_length=150, blank=True)
    email = EmailField(blank=True)
    is_staff = BooleanField(default=False)
    is_active = BooleanField(default=False)
    is_blocked = BooleanField(db_default=False)
    last_activity = DateTimeField(auto_now_add=True)

    created_at = DateTimeField(auto_now=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]


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

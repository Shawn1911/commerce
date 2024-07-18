from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import CharField, ForeignKey, CASCADE, TextField, IntegerField, FloatField, BooleanField, \
    DateTimeField, OneToOneField, EmailField, SET_NULL, BigIntegerField, TextChoices, RESTRICT, Model

from shared.django.models import CreatedBaseModel


class Person(Model):
    name = CharField(max_length=255)
    phone = CharField(max_length=25)

#
# class ShopUser(AbstractBaseUser, PermissionsMixin):  # ?
#     class Type(TextChoices):
#         EMAIL = 'email', 'Email'
#         TELEGRAM = 'telegram', 'Telegram'
#         FACEBOOK = 'facebook', 'Facebook'
#
#     username = CharField(max_length=150, unique=True, validators=[UnicodeUsernameValidator()])
#
#     last_activity = DateTimeField(auto_now_add=True)
#     is_blocked = BooleanField(db_default=False)
#     telegram_id = BigIntegerField(blank=True, null=True, unique=True)
#     person = OneToOneField('users.Person', SET_NULL, null=True, blank=True)
#
#     type = CharField(max_length=25)
#     first_name = CharField(max_length=150, blank=True)
#     last_name = CharField(max_length=150, blank=True)
#     email = EmailField(blank=True)
#     is_staff = BooleanField(default=False)
#     is_active = BooleanField(default=False)
#
#     language = ForeignKey('shops.Language', CASCADE)
#     shop = ForeignKey('shops.Shop', CASCADE, related_name='customers')
#     created_at = DateTimeField(auto_now=True)
#     # messages (count)
#     # orders_count (count)
#
#     objects = UserManager()
#
#     EMAIL_FIELD = "email"
#     REQUIRED_FIELDS = ["email"]
#
#     class Meta:
#         unique_together = [
#             ('username', 'shop')
#         ]


class User(AbstractBaseUser, PermissionsMixin):  # ?
    class Type(TextChoices):
        EMAIL = 'email', 'Email'
        TELEGRAM = 'telegram', 'Telegram'
        FACEBOOK = 'facebook', 'Facebook'

    type = CharField(max_length=25)
    username = CharField(max_length=150, unique=True, validators=[UnicodeUsernameValidator()])
    first_name = CharField(max_length=150, blank=True)
    last_name = CharField(max_length=150, blank=True)
    email = EmailField(blank=True)
    is_staff = BooleanField(default=False)
    is_active = BooleanField(default=False)

    language = ForeignKey('shops.Language', CASCADE)
    public_offer = BooleanField(default=False)
    invitation_code = CharField(max_length=25, unique=True, null=True)
    created_at = DateTimeField(auto_now=True)
    default_shop = OneToOneField('shops.Shop', SET_NULL, blank=True, null=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]


class Plan(CreatedBaseModel):
    class PeriodType(TextChoices):
        MONTHLY = 'monthly', 'Monthly'
        ANNUAL = 'annual', 'Annual'

    period_type = CharField('Davr turi', max_length=25, choices=PeriodType.choices, db_default=PeriodType.MONTHLY)
    code = CharField('Kod', max_length=150)
    name = CharField('Nomi', max_length=150)
    description = TextField('Tavsif', max_length=150)
    day = IntegerField(db_default=0)
    expires_at = DateTimeField()
    status = BooleanField(default=False)


class PlanPricing(CreatedBaseModel):
    price = FloatField('Narxi', db_default=0)
    original_price = FloatField('Haqiqiy narxi', db_default=0)
    name = CharField('Nomi', max_length=50)
    period = IntegerField('Davr', db_default=30)
    currency = ForeignKey('shops.Currency', RESTRICT)
    plan = ForeignKey('users.Plan', CASCADE)


class PlanQuotas(CreatedBaseModel):
    name = CharField('Nomi', max_length=150)
    description = TextField('Tavsif', null=True, blank=True)
    value = CharField('Qiymat', max_length=50, null=True, blank=True)
    plan = ForeignKey('users.Plan', CASCADE)

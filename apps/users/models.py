from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager,)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import (CASCADE, RESTRICT, SET_NULL, BigIntegerField,
                              BooleanField, CharField, DateField,
                              DateTimeField, EmailField, ForeignKey,
                              IntegerField, ManyToManyField, Model,
                              OneToOneField, PositiveIntegerField, TextChoices,
                              TextField, URLField,)
from shared.django.models import CreatedBaseModel
from users.managers import CustomUserManager


class Person(Model):  # ✅
    name = CharField(max_length=255)
    phone = CharField(max_length=25)


class ShopUser(AbstractBaseUser):  # ✅
    class Type(TextChoices):
        EMAIL = 'email', 'Email'
        TELEGRAM = 'telegram', 'Telegram'
        FACEBOOK = 'facebook', 'Facebook'

    username = CharField(max_length=150, unique=True, validators=[UnicodeUsernameValidator()])

    last_activity = DateTimeField(auto_now_add=True)
    is_blocked = BooleanField(db_default=False)
    telegram_id = BigIntegerField(blank=True, null=True, unique=True)
    person = OneToOneField('users.Person', SET_NULL, null=True, blank=True)

    type = CharField(max_length=25)
    first_name = CharField(max_length=150, blank=True)
    last_name = CharField(max_length=150, blank=True)
    email = EmailField(blank=True)
    is_staff = BooleanField(default=False)
    is_active = BooleanField(default=False)

    language = ForeignKey('shops.Language', CASCADE)
    shop = ForeignKey('shops.Shop', CASCADE, related_name='customers')
    created_at = DateTimeField(auto_now=True)
    # messages (count)
    # orders_count (count)

    objects = UserManager()

    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        unique_together = [
            ('username', 'shop')
        ]


class User(AbstractBaseUser, PermissionsMixin):  # ✅
    class Type(TextChoices):
        EMAIL = 'email', 'Email'
        TELEGRAM = 'telegram', 'Telegram'
        FACEBOOK = 'facebook', 'Facebook'

    type = CharField(max_length=25)
    username = CharField('Foydalanuvchi nomi', max_length=150, null=True, blank=True, unique=True,
                         validators=[UnicodeUsernameValidator()])
    first_name = CharField('Ism', max_length=150, blank=True)
    last_name = CharField('Familiya', max_length=150, blank=True)
    email = EmailField('Email', unique=True)
    is_staff = BooleanField(default=False)
    is_active = BooleanField(default=False)
    linked_account = ManyToManyField('users.LinkedAccount', through='UserLinkedAccount', related_name='accounts')
    language = ForeignKey('shops.Language', CASCADE, blank=True, null=True)
    public_offer = BooleanField('Ommaviy taklif', default=False)
    invitation_code = CharField('Taflifnoma kodi', max_length=25, unique=True, null=True)
    created_at = DateTimeField(auto_now=True)
    default_shop = OneToOneField('shops.Shop', SET_NULL, blank=True, null=True)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Plan(CreatedBaseModel):  # ✅
    name = CharField('Nomi', max_length=150)
    code = CharField('Kod', max_length=150)
    description = TextField('Tavsif', max_length=150)
    quotas = ManyToManyField('users.Quotas', through='users.PlanQuotas', blank=True)


class PlanPricing(CreatedBaseModel):  # ✅
    class PeriodType(TextChoices):
        MONTHLY = 'monthly', 'Monthly'
        ANNUAL = 'annual', 'Annual'

    name = CharField('Nomi', max_length=50)
    period_type = CharField('Davr turi', max_length=25, choices=PeriodType.choices, db_default=PeriodType.MONTHLY)
    currency = ForeignKey('shops.Currency', RESTRICT)

    price = PositiveIntegerField('Narxi')
    original_price = PositiveIntegerField('Haqiqiy narxi')
    period = IntegerField('Davr')
    plan = ForeignKey('users.Plan', CASCADE)


class Quotas(CreatedBaseModel):  # ✅
    name = CharField('Nomi', max_length=150)
    description = TextField('Tavsif', blank=True)


class PlanQuotas(Model):
    plan = ForeignKey('users.Plan', CASCADE)
    quotas = ForeignKey('users.Quotas', CASCADE)
    value = CharField('Qiymat', max_length=50)


class PlanInvoice(CreatedBaseModel):  # ✅
    class Status(TextChoices):
        NEW = 'new', 'New'
        COMPLETED = 'completed', 'Completed'

    price = CharField('Narxi', max_length=55)
    user = ForeignKey('users.User', CASCADE, related_name='plan_invoices')
    plan = ForeignKey('users.Plan', CASCADE)
    payed_at = DateTimeField('da toʻlangan', null=True, blank=True)
    pay_url = URLField('tolov url', null=True, blank=True)
    plan_extended_from = DateField()
    plan_extended_until = DateField(null=True, blank=True)
    status = CharField(max_length=25, choices=Status.choices, db_default=Status.NEW)


class LinkedAccount(Model):
    name = CharField(max_length=40)


class UserLinkedAccount(Model):
    status = BooleanField(db_default=False)
    user = ForeignKey('users.User', CASCADE, related_name='accounts')
    linked = ForeignKey('users.LinkedAccount', CASCADE)

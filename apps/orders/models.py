from django.db.models import Model, CharField, ForeignKey, CASCADE, TextField, TextChoices, IntegerField, BooleanField, \
    JSONField, DateTimeField, PositiveIntegerField, ManyToManyField, SET_NULL
from shared import CreatedBaseModel


class Order(CreatedBaseModel):
    class Status(TextChoices):
        REFUNDED = 'refunded', 'Refunded'
        ARCHIVED = 'archived', 'Archived'
        IN_PROCESSING = 'in_processing', 'In Processing'

    class Type(TextChoices):
        TELEGRAM = 'telegram', 'Telegram'
        WEB = 'web', 'Web'

    type = CharField(max_length=25, choices=Type.choices)
    status = CharField(max_length=25, choices=Status.choices, db_default=Status.IN_PROCESSING)
    promo_code = ForeignKey('orders.PromoCode', SET_NULL, null=True, blank=True, related_name='orders')
    user = ForeignKey('users.User', CASCADE, related_name='orders')
    note = CharField(max_length=255, null=True, blank=True)


class PromoCode(CreatedBaseModel):  # ✅
    class Type(TextChoices):
        FREE_DELIVERY = 'free_delivery', 'Free delivery'
        DISCOUNT = 'discount', 'Discount'

    active = BooleanField(default=True)
    code = CharField(max_length=255, unique=True)
    start_date = DateTimeField()
    end_date = DateTimeField()
    limit = IntegerField()
    remaining_quantity = IntegerField()
    type = CharField(max_length=255, choices=Type.choices, default=Type.FREE_DELIVERY)
    percent = IntegerField(db_default=0)
    used_quantity = PositiveIntegerField()
    shop = ForeignKey('shops.Shop', CASCADE, related_name='promo_codes')

    class Meta:
        verbose_name = 'Promo kod'
        verbose_name_plural = 'Promo kodlar'


class ShopService(Model):  # ✅
    class Status(TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        NOT_EXISTS = 'not_exists', 'Not exists'

    shop = ForeignKey('shops.Shop', CASCADE)
    service = ForeignKey('orders.Service', CASCADE)
    status = CharField(max_length=15, choices=Status.choices, db_default=Status.INACTIVE)
    fields = ManyToManyField('orders.Field', through='orders.ShopServiceField')


class Service(Model):  # ✅
    class ServiceType(TextChoices):
        DELIVERY = 'delivery', 'Delivery'
        PAYMENT = 'payment', 'Payment'

    class Type(TextChoices):
        INTERNAL = 'internal', 'Internal'
        INPLACE = 'inplace', 'Inplace'
        TELEGRAM = 'telegram', 'Telegram'
        WEB = 'web', 'Web'
        INSTALMENT = 'instalment', 'Instalment'

    service_type = CharField(max_length=15, choices=ServiceType.choices)
    title = CharField(max_length=255)
    code = CharField(max_length=255)
    type = CharField(max_length=255, choices=Type.choices)
    description = TextField(null=True, blank=True)

    class Meta:
        unique_together = [
            ('code', 'type')
        ]


class ShopServiceField(Model):  # ✅
    shop_service = ForeignKey('shops.ShopService', CASCADE)
    field = ForeignKey('shops.Field', CASCADE)
    value = JSONField(default=dict)


class Field(Model):  # ✅
    class Type(TextChoices):
        INTEGER = 'integer', 'Integer'
        STRING = 'string', 'String'
        TEXT = 'text', 'Text'
        LIST = 'list', 'List'
        VIDEO = 'video', 'Video'
        IMAGE = 'image', 'Image'
        GEOLOCATION = 'geolocation', 'Geolocation'

    service = ForeignKey('orders.Service', CASCADE, related_name='fields')
    label = CharField(max_length=255)
    name = CharField(max_length=255, unique=True)
    max_length = IntegerField()
    required = BooleanField()
    type = CharField(max_length=255, choices=Type.choices)
    provider_labels = JSONField(null=True, blank=True)

from django.db.models import Model, CharField, ForeignKey, CASCADE, TextField, TextChoices, IntegerField, BooleanField, \
    JSONField, DateTimeField, PositiveIntegerField
from shared import CreatedBaseModel


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


class Service(Model):  # ✅
    class Type(TextChoices):
        INTERNAL = 'internal', 'Internal'
        INPLACE = 'inplace', 'Inplace'
        TELEGRAM = 'telegram', 'Telegram'
        WEB = 'web', 'Web'
        INSTALMENT = 'instalment', 'Instalment'

    title = CharField(max_length=255)
    code = CharField(max_length=255)
    type = CharField(max_length=255, choices=Type.choices)
    description = TextField(null=True, blank=True)

    class Meta:
        unique_together = [
            ('code', 'type')
        ]

# class PaymentField(Model):
#     class Type(TextChoices):
#         INTEGER = 'integer', 'Integer'
#         STRING = 'string', 'String'
#         TEXT = 'text', 'Text'
#         LIST = 'list', 'List'
#
#     payment_provider = ForeignKey('shops.PaymentProvider', CASCADE, related_name='payment_field')
#     label = CharField(max_length=255)
#     name = CharField(max_length=255, unique=True)
#     required = BooleanField()
#     type = CharField(max_length=255, choices=Type.choices)
#     value = CharField(max_length=255)
#     provider_labels = JSONField()
#
#
# class DeliveryField(Model):
#     class Type(TextChoices):
#         STRING = 'string', 'String'
#         VIDEO = 'video', 'Video'
#         IMAGE = 'image', 'Image'
#         TEXT = 'text', 'Text'
#         INTEGER = 'integer', 'Integer'
#
#     delivery = ForeignKey('shops.DeliveryService', CASCADE, verbose_name='Yetkazish xizmati')
#     label = CharField(max_length=255, null=True, blank=True)
#     name = CharField(max_length=255, null=True, blank=True)
#     required = BooleanField(db_default=True, default=True)
#     type = CharField(max_length=20, choices=Type.choices)
#     value = JSONField(default=dict)
